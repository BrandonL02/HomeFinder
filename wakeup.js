// wakeup.js
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: "new",  // Use "true" if "new" doesn't work in your Node version
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.goto('https://homefinder-tampa.streamlit.app/', {
    waitUntil: 'networkidle2',
    timeout: 0
  });

  // Optional: click the "wake up" button if it's visible
  try {
    await page.waitForSelector('button', { timeout: 10000 });
    const buttonText = await page.evaluate(() => {
      const button = document.querySelector('button');
      return button?.innerText || '';
    });

    if (buttonText.includes('Yes, get this app back up!')) {
      await page.click('button');
      console.log('Wake up button clicked!');
    } else {
      console.log('No wake-up button found; app is already up.');
    }
  } catch (err) {
    console.log('No button found or page is already up.');
  }

  await browser.close();
})();
