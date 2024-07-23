browser.tabs.onActivated.addListener((activeInfo) => {
    console.log("Tab " + activeInfo.tabId + " was activated");
  });
  