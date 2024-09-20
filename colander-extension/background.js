browser.tabs.onActivated.addListener((activeInfo) => {
    console.log("Tab " + activeInfo.tabId + " was activated");
  });
  
function sendNativeMessage(message) {
  browser.runtime.sendNativeMessage("colander_native_messaging", message)
    .then(response => {
      console.log("Received response: ", response);
    })
    .catch(error => {
      console.error("Error: ", error);
    });
}

function testNativeMessaging() {
  browser.runtime.sendNativeMessage("colander_native_messaging", { action: "test" })
    .then(response => {
      console.log("Received response:", response);
    })
    .catch(error => {
      console.error("Native messaging error:", error);
    });
}

browser.runtime.onInstalled.addListener(testNativeMessaging);

// tab data preparation
function prepareTabData(tab) {
  return {
    id: tab.id,
    url: tab.url,
    title: tab.title,
    active: tab.active
  };
}

// chunking logic
const CHUNK_SIZE = 5; // Start with retrieving 5 tabs at a time
let allTabs = [];
let currentIndex = 0;

function getNextChunk() {
  browser.tabs.query({}).then((tabs) => {
    allTabs = tabs;
    processChunk();
  });
}

function processChunk() {
  const chunk = allTabs.slice(currentIndex, currentIndex + CHUNK_SIZE);
  currentIndex += CHUNK_SIZE;

  chunk.forEach(tab => {
    // Process each tab in the chunk
    console.log(`Processing tab: ${tab.title}`);
    // Here you would implement your tab processing logic
  });
  
  if (currentIndex < allTabs.length) {
    // If there are more tabs, schedule the next chunk
    setTimeout(processChunk, 100); // Add a small delay to prevent blocking
  } else {
    console.log("All tabs processed");
  }

  const processedChunk = chunk.map(prepareTabData);

  browser.runtime.sendNativeMessage("colander_native_messaging", {
    action: "process_tabs",
    data: processedChunk
  }).then(response => {
    console.log("Chunk processed by Python backend:", response);
    if (currentIndex < allTabs.length) {
      setTimeout(processChunk, 100);
    } else {
      console.log("All tabs processed");
    }
  }).catch(error => {
    console.error("Error sending chunk to Python backend:", error);
  });
}

// Trigger the chunking process
browser.browserAction.onClicked.addListener(getNextChunk);