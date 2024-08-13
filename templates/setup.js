var bot = new ChatSDK({
    config: {
      navbar: {
        title: '智能助理'
      },
      robot: {
        avatar: '//gw.alicdn.com/tfs/TB1U7FBiAT2gK0jSZPcXXcKkpXa-108-108.jpg'
      },
      messages: [
        {
          code: 'text',
          data: {
            text: '智能助理为您服务，请问有什么可以帮您？'
          }
        }
      ]
    },
    requests: {
      send: function (msg) {
        if (msg.type === 'text') {
          return {
            url: '//api.server.com/ask',
            data: {
              q: msg.content.text
            }
          };
        }
      }
    }
  });
  
  bot.run();