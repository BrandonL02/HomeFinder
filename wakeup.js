const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();

  await page.goto('https://homefinder-tampa.streamlit.app/', {
    waitUntil: 'networkidle2',
    timeout: 0,
  });

  try {
    // Wait up to 10 seconds for the wake-up button to appear
    await page.waitForSelector('button', { timeout: 10000 });

    // Find the button with the exact or partial text
    const buttonHandle = await page.$x("//button[contains(., 'Yes, get this app back up!')]");

    if (buttonHandle.length > 0) {
      await buttonHandle[0].click();
      console.log('Wake up button clicked!');
    } else {
      console.log('Wake up button not found - app may already be active.');
    }
  } catch (error) {
    console.log('Button not found within timeout, assuming app is already active.');
  }

  await browser.close();
})();
