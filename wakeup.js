const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  console.log('💤 Checking if app needs waking up...');

  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();

  await page.goto('https://homefinder-tampa.streamlit.app/', {
    waitUntil: 'domcontentloaded',
    timeout: 0,
  });

  // Wait extra time for any JS rendering to finish
  await page.waitForTimeout(5000);

  // Save screenshot and HTML for debugging
  const saveDebug = async () => {
    await page.screenshot({ path: 'debug.png', fullPage: true });
    const html = await page.content();
    fs.writeFileSync('debug.html', html);
    console.log('📝 Saved debug.png and debug.html');
  };

  try {
    const selector = 'button[data-testid="wakeup-button-owner"]';

    const button = await page.$(selector);

    if (button) {
      await button.click();
      console.log('✅ Button found and clicked: app is waking up!');
    } else {
      console.log('ℹ️ No button found — app is already awake.');
    }
  } catch (error) {
    console.error('❌ Error during Puppeteer execution:', error.message);
  }

  await saveDebug();
  await browser.close();
})();
