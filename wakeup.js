const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: false, slowMo: 50 }); // Set headless: false to debug
  const page = await browser.newPage();

  await page.goto('https://homefinder-tampa.streamlit.app/', {
    waitUntil: 'domcontentloaded',
    timeout: 0,
  });

  try {
    // Wait for the button using its unique data-testid
    await page.waitForSelector('button[data-testid="wakeup-button-owner"]', { timeout: 15000 });

    const button = await page.$('button[data-testid="wakeup-button-owner"]');
    if (button) {
      await button.click();
      console.log('Clicked the wake-up button!');
    } else {
      console.log('Button not found.');
    }
  } catch (error) {
    console.log('Error:', error.message);
  }

  await browser.close();
})();
