document.addEventListener('DOMContentLoaded', function () {
    //Alpine.start();
    htmx.logAll();
});

function getData() {
    return {
      responseData: null,
      ipdata:null,
      async fetchData() {
        try {
          const response = await fetch('/run?command=cat /var/log/syslog'); // Replace with your API endpoint
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          const data = await response.json();
          data.resulttxt = data.result;
          data.result = data.result.split('\n');
          this.responseData = data;
          // Print responseData to the console
          console.log(data.result);
        } catch (error) {
          console.error('Error:', error);
        }
      },
      async fetchData2() {
        try {
          const response = await fetch('/ipaddr'); // Replace with your API endpoint
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          const data = await response.json();
          this.ipdata = data;
          // Print responseData to the console
          console.log(data.result);
        } catch (error) {
          console.error('Error:', error);
        }
      },
      download() {
        //let text = JSON.stringify(this.responseData.resulttxt);
        this.fetchData();
        let text = this.responseData.resulttxt;
        let filename = 'log.txt';
        let element = document.createElement('a');
        element.setAttribute('href', 'data:application/txt;charset=utf-8,' + encodeURIComponent(text));
        element.setAttribute('download', filename);
        element.click();
    },
    
    };
  }
