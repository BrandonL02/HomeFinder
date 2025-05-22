const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();

  await page.goto('https://homefinder-tampa.streamlit.app/', {
    waitUntil: 'networkidle2',
    timeout: 0,
  });

  try {
    // Wait for the button at the XPath
    await page.waitForXPath('/html/body/div[1]/div[1]/div/div/div/div/button', { timeout: 10000 });

    // Get the button element handle
    const [button] = await page.$x('/html/body/div[1]/div[1]/div/div/div/div/button');

    if (button) {
      await button.click();
      console.log('Clicked the wake-up button!');
    } else {
      console.log('Wake-up button not found - app may already be active.');
    }
  } catch (error) {
    console.log('Wake-up button not found or timeout reached, assuming app is already active.');
  }

  await browser.close();
})();
