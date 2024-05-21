// pages/search/search.js
const utils = require('../../utils/common.js') //添加引用

Page({
  data: {
    inputValue: '', // 输入框的值
    requestStatus: false, // 是否成功获取信息
    status: null, // 获取到的开水机状态
    number: null, // 获取到的排队人数
  },

  // 输入框内容改变时触发
  inputChange: function (e) {
    this.setData({
      inputValue: e.detail.value,
    });
  },

  // 点击搜索按钮时触发
  search: async function () {
    // 向服务器发起请求
    try {
      var status = await utils.getStatus(this.data.inputValue); // 使用 await 调用 getStatus
      console.log(`status: ${status}`);
      var number = await utils.getNumber(this.data.inputValue);
      console.log(`number: ${number}`);
      this.setData({
        status: status,
        number: number,
        requestStatus: true
      })
    } catch (err) {
      console.log(`${err}`);
      this.setData({
        requestStatus: false
      })
    }
  },
});
