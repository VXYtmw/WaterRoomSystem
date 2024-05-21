// utils/common.js

// 请求开水机状态信息
function getStatus(id) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: `http://X.X.X.X:443/api/get_status?id=${id}`, // 请求地址
      method: 'GET', // 请求方法
      success(res) {
        if (res.statusCode === 200) {
          // 请求成功
          resolve(res.data.status); 
        } else {
          // 请求失败
          reject(new Error(`Request failed with status code ${res.statusCode}`));
        }
      },
      fail(err) {
        // 请求失败
        reject(err);
      }
    });
  });
}

// 请求排队人数信息
function getNumber(id) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: `http://X.X.X.X:443/api/get_number?id=${id}`, // 请求地址     method: 'GET', // 请求方法
      success(res) {
        if (res.statusCode === 200) {
          resolve(res.data.number); 
        } else {
          reject(new Error(`Request failed with status code ${res.statusCode}`));
        }
      },
      fail(err) {
        reject(err);
      }
    });
  });
}

//暴露接口供外部调用
module.exports = {
  getStatus,
  getNumber
}
