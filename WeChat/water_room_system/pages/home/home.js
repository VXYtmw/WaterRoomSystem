// pages/home/home.js
const utils = require('../../utils/common.js') //添加引用

Page({
  data: {
    // 获取到的信息结果
    results: {
      1: {},
      2: {},
      3: {},
    },
    requestInterval: null // 页面定时器，用于发起请求
  },

  onShow() {
    this.getInfo();
    this.data.requestInterval = setInterval(()=>
    {
      console.log("定时更新数据");
      this.getInfo();
    }, 10000);
  },

  onHide() {
    clearInterval(this.data.requestInterval); 
  },

  getInfo: async function() {
    for (const id in this.data.results) {
      try {
        var status = await utils.getStatus(id); // 使用 await 调用 getStatus
        console.log(`id: ${id} status: ${status}`);
        var number = await utils.getNumber(id);
        console.log(`id: ${id} number: ${number}`);
        this.setData({
          [`results.${id}`]: {id: id, status: status, number: number}
        });
      } catch (err) {
        console.log(`${err}`);
        this.setData({
          requestStatus: false
        })
      }
    }
  }
})