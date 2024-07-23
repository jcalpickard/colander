document.getElementById('colanderButton').addEventListener('click', () => {
    browser.tabs.query({active: true, currentWindow: true})
      .then((tabs) => {
        let tab = tabs[0];
        let info = `Title: ${tab.title}\nURL: ${tab.url}`;
        document.getElementById('tabInfo').textContent = info;
      })
      .catch((error) => {
        console.error(`Error: ${error}`);
      });
  });
  