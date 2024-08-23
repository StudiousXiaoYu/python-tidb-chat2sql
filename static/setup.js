/* eslint-disable prefer-destructuring */
/* 示例代码，不经过编译直接输出，注意代码浏览器兼容性 */
(function () {
  let ua = navigator.userAgent;
  let isInApp = ua.indexOf('dtdream') !== -1;
  let iOS = /iPad|iPhone|iPod/.test(ua);

  if (isInApp && iOS) {
    document.documentElement.style.height = `${window.innerHeight}px`;
  }  
  let requests = {
    baseUrl: 'https://app.zjzwfw.gov.cn/jfaqfront',
    send: function send(msg) {
      let context = bot.getContext();
      let sessionId = 'M9u913BFyxIuTdRv7O73nx9SfkWgerhk';

      return {
        url: '/xiaomi/ask.do',
        data: {
          q: msg.content.text,
          areakey: context.location.key,
          sessionId: sessionId,
          instanceId: 1071,
        },
      };
    },  
  };

  let handlers = {
    parseResponse: function parseResponse(res, requestType) {
      if (requestType === 'send' && res.Messages) {
        return window.isvParser({
          data: res,
          noAnswer: [
            zwBundle.makeCardMsg('knowledge', {
              text: `抱歉，您的问题我暂时答不上来。您可以${consultUrl}进行表单提交，或在下方切换区域后再进行询问。`,
            }),
            zwBundle.makeCardMsg('switch-location'),
          ],
          evaluableCodeList: ['knowledge', 'guidance'],
        });
      }

      if (requestType === 'autoComplete') {
        return {
          list: res.AssociateList.slice(0, 8).map((t) => {
            return {
              title: t.Title,
            };
          }),
          keyword: res.Utterance,
        };
      }
      return res;
    },
    // renderRateActions,
  };
  const consultUrl = isInApp
    ? '<form style="display:inline" action="https://zjzxtsjbpt.yyhj.zjzwfw.gov.cn/zhejiang/m/gotoZiXun.json" method="post"><button style="margin:0;padding:0;border:0;background:transparent;color:var(--blue);">点击这里</button></form>'
    : '<a href="http://www.zjzxts.gov.cn/wsdt.do?method=suggest&xjlb=0&ymfl=1&uflag=1">点击这里</a>';
  const components = window.zwBundle.components;
  components.brand = components.header;
  const bot = new ChatSDK({
    config: {
      brand: {
        logo: 'https://gw.alicdn.com/tfs/TB1Wbldh7L0gK0jSZFxXXXWHVXa-168-33.svg',
        url: 'http://hzyh.zjzwfw.gov.cn/',
        title: '浙江政务服务网',
        name: '智能助理',
      },
      robot: {
        avatar:
          'https://gw.alicdn.com/tfs/TB1U7FBiAT2gK0jSZPcXXcKkpXa-108-108.jpg',
      },
      quickReplies: [
        {
          name: '健康码颜色',
        },
        {
          name: '入浙通行申报',
        },
        {
          name: '健康码是否可截图使用',
        },
        {
          name: '健康通行码适用范围',
        },
        {
          name: '最美战疫人有哪些权益',
        },
        {
          name: '我要查社保',
        },
        {
          name: '办理居住证需要什么材料',
        },
        {
          name: '公共支付平台',
        },
        {
          name: '浙江省定点医院清单',
        },
        {
          name: '智能问诊',
        },
      ],
      placeholder: '输入任何您想办理的服务',
      sidebar: [
        {
          code: 'sidebar-suggestion',
          data: [
            {
              label: '疫情问题',
              list: [
                '身边有刚从湖北来的人，如何报备',
                '接触过武汉人，如何处理？',
                '发烧或咳嗽怎么办？',
                '去医院就医时注意事项',
                '个人防护',
                '传播途径',
                '在家消毒',
              ],
            },
            {
              label: '法人问题',
              list: [
                '企业设立',
                '企业运行',
                '企业变更',
                '企业服务',
                '企业注销',
                '社会团体',
                '民办非企业',
              ],
            },
          ],
        },
        {
          code: 'sidebar-tool',
          title: '常用工具',
          data: [
            {
              name: '咨询表单',
              icon: 'clipboard-list',
              url: 'http://www.zjzxts.gov.cn/wsdt.do?method=suggest&xjlb=0&ymfl=1&uflag=1',
            },
            {
              name: '投诉举报',
              icon: 'exclamation-shield',
              url: 'http://www.zjzxts.gov.cn/wsdt.do?method=suggest&xjlb=1',
            },
            {
              name: '办事进度',
              icon: 'history',
              url: 'http://www.zjzwfw.gov.cn/zjzw/search/progress/query.do?webId=1',
            },
          ],
        },
        {
          code: 'sidebar-phone',
          title: '全省统一政务服务热线',
          data: ['12345'],
        },
      ],
      feedback: {
        multiple: true,
        modalable: false,
        needFeedback: true,
      },
    },
    requests: requests,
    handlers: handlers,
    components: components,
  });
  bot.run();
  const ctx = bot.getCtx();
  console.log('ctx:', ctx);
  window.bot = bot;
})();
