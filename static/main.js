document.addEventListener('DOMContentLoaded', function () {
    //Alpine.start();
});

function getData() {
    return {
      responseData: null,
      async fetchData() {
        try {
          const response = await fetch('/run?command=df'); // Replace with your API endpoint
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          const data = await response.json();
          this.responseData = data;
          // Print responseData to the console
          console.log(this.responseData);
        } catch (error) {
          console.error('Error:', error);
        }
      },
    };
  }
  