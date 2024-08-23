(function () {
const components = window.zwBundle;
console.log('cents:', window);
var bot = new ChatSDK({
  config: {
      navbar: {
          title: 'SQL管家助理'
      },
      avatarWhiteList: ['all'],
      robot: {
          avatar: '/static/tidb.png'
      },
      // 用户头像
      user: {
          avatar: '/static/boy.png',
      },
      quickReplies: [
        {
          name: '学生信息表结构',
        },
        {
          name: '执行简单SQL',
          type: 'text',
          text: '/execute select * from Students;',
          isNew: true,
        },
      ],
      placeholder: '输入任何您想要咨询的SQL语句',
      messages: [
          {
              code: 'text',
              data: {
                  text: '欢迎使用SQL管家服务，请输入您的问题，我将为您生成相应的SQL语句？'
              }
          }
      ],
      // sidebar: [
      //     { 
      //         title: '欢迎使用SQL管家',
      //         code: 'text',
      //         data: {
      //             text: "欢迎使用SQL管家服务，请输入您的问题，我将为您生成相应的SQL语句？",
      //         }
      //     },
      // ],
  }, 
  requests: {
      send: function (msg) {
      if (msg.type === 'text') {
          return {
          url: 'http://127.0.0.1:3000/ask',
          data: {
              query: msg.content.text
          },
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
              }
          };
      }
      }
  },
  handlers: {
      parseResponse: function (res, requestType) {
          return {
              code: 'foundation-model',
              data: res
              // data: {
              //     answerReference: {
              //         itemList: [
              //             {
              //                 content:
              //                 '<p>阿里云官网链接是： https：//www.aliyun.com/ 或者是 https：//aliyun.com\n对话机器人 POC 环境地址是： http：//poc-console.alixiaomi.com：8081/\n</p>',
              //                 contentType: 'RICH_TEXT',
              //                 dataSource: 'doc',
              //                 docName: '123链接',
              //                 number: 1,
              //                 originNumber: 1,
              //                 pagePos: [
              //                 {
              //                     height: 29,
              //                     pageId: '1',
              //                     width: 779,
              //                     x: 203,
              //                     y: 167,
              //                 },
              //                 ],
              //                 title: '123文档',
              //             },
              //         ],
              //     },
              //     content: res.data,
              //     sentenceList: [
              //         {
              //         content: res.data,
              //         referNumber: 1,
              //         },
              //     ],
              //     streamEnd: true,
              // }
          };
      }
  }
  ,
  // components: {
  //   // 组件名称对应side-bar配置中的code
  //   'sidebar-suggestion': (props) => {
  //     if (!props.data?.length) {
  //       return null;
  //     }
  //     return (<div>
  //       <div>{props.data[0].label}</div>
  //       <div>{props.data[0].list?.map((one,index) => {
  //         return <p key={index}>{one}</p>
  //       })}</div>
  //     </div>)
  //   }
  // }
});
  bot.run();
  const ctx = bot.getCtx();
  console.log('ctx:', ctx);
  window.bot = bot;
})();
