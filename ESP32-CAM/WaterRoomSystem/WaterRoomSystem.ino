#include <Arduino.h>
#include <WiFi.h>
#include "esp_camera.h"
#include <vector>

// #define LIGHT_SIMULATE  // 启用光敏传感器数据模拟

const char *ssid = "";  // WiFi名称
const char *password = "";  // WiFi密码
const IPAddress serverIP(X,X,X,X);  // 服务器地址
uint16_t serverPort = 8080;  // 服务器端口号
uint16_t pinLight = 12;  // 光敏传感器引脚
uint8_t waterRoomID = 3;  // 开水房ID号
bool light = 0;
uint16_t sendTime = 30000;  // 发送一轮信息的延时（ms）
 
#define maxcache 1430  // 应用层设置的分包大小
 
WiFiClient client; // 声明一个客户端对象，用于与服务器进行连接
 
// CAMERA_MODEL_AI_THINKER类型摄像头的引脚定义
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
 
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22
 
static camera_config_t camera_config = {
    .pin_pwdn = PWDN_GPIO_NUM,
    .pin_reset = RESET_GPIO_NUM,
    .pin_xclk = XCLK_GPIO_NUM,  
    .pin_sscb_sda = SIOD_GPIO_NUM,
    .pin_sscb_scl = SIOC_GPIO_NUM,
    
    .pin_d7 = Y9_GPIO_NUM,
    .pin_d6 = Y8_GPIO_NUM,
    .pin_d5 = Y7_GPIO_NUM,
    .pin_d4 = Y6_GPIO_NUM,
    .pin_d3 = Y5_GPIO_NUM,
    .pin_d2 = Y4_GPIO_NUM,
    .pin_d1 = Y3_GPIO_NUM,
    .pin_d0 = Y2_GPIO_NUM,
    .pin_vsync = VSYNC_GPIO_NUM,
    .pin_href = HREF_GPIO_NUM,
    .pin_pclk = PCLK_GPIO_NUM,
    
    .xclk_freq_hz = 20000000,  // 时钟频率
    .ledc_timer = LEDC_TIMER_0,
    .ledc_channel = LEDC_CHANNEL_0,
    
    .pixel_format = PIXFORMAT_JPEG,
    .frame_size = FRAMESIZE_VGA,  // 图片格式
    .jpeg_quality = 12,  // JPEG图片质量，0-63，数字越小质量越高。12的分辨率为640*480
    .fb_count = 1,
};

void wifi_init()
{
    WiFi.mode(WIFI_STA);
    WiFi.setSleep(false);  // 关闭STA模式下wifi休眠，提高响应速度
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println("WiFi Connected!");
    Serial.print("IP Address:");
    Serial.println(WiFi.localIP());
}

esp_err_t camera_init() {
    esp_err_t err = esp_camera_init(&camera_config);
    if (err != ESP_OK) {
        Serial.println("Camera Init Failed");
        return err;
    }
    Serial.println("Camera Init OK!");
    return ESP_OK;
}
 
void setup()
{
    Serial.begin(115200);
    wifi_init();  // 初始化WiFi模块
    camera_init();  // 初始化摄像模块
}


void loop()
{
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
    Serial.println("Try To Connect TCP Server");
    if (client.connect(serverIP, serverPort))  // 尝试访问目标地址
    {
        Serial.println("Connect Tcp Server Success!");
        client.write(waterRoomID);  // 发送开水房ID

        while (client.connected()) {
          #ifdef LIGHT_SIMULATE
          light = !light;
          #else
          light = !digitalRead(pinLight);
          #endif
          camera_fb_t * fb = esp_camera_fb_get();  // 获取摄像模块头帧
          uint8_t * temp = fb->buf;  // 保存摄像模块头帧内容的起始指针
          if (!fb)
          {
              Serial.println("Camera Capture Failed");
          }
          else
          {
            // 先发送光敏传感器数据
            // 再发送 Frame Begin 表示开始发送图片数据，完毕后发送 Frame Over 表示发送结束
            // 图片数据分包发送，每次发送1430字节
            client.write(light);  // 发送光敏传感器数据
            Serial.print("Success To Send Light Information. Status: ");
            Serial.println(light);
            client.print("Frame Begin");  // 开始发送图片数据
            // 将图片数据分段发送
            int leng = fb->len;
            int times = leng / maxcache;
            int extra = leng % maxcache;
            for(int j = 0; j < times; j++)
            {
              client.write(fb->buf, maxcache); 
              for (int i = 0; i < maxcache; i++)
              {
                fb->buf++;
              }
            }
            client.write(fb->buf, extra);
            client.print("Frame Over");  // 结束发送图片数据
            Serial.print("Succes To Send Image. This Frame Length: ");
            Serial.println(fb->len);

            delay(sendTime);

            fb->buf = temp;  // 返回保存的指针
            esp_camera_fb_return(fb);  // 返回头帧
          }
        }
        // Serial.println("Close Connect!");
        // client.stop();  //关闭客户端
    }
    else
    {
      client.stop();  //关闭客户端
    }
    Serial.println("Connect To Tcp Server Failed! After 10 Seconds Try Again!");
    delay(10000);
}