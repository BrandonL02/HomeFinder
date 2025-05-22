const puppeteer = require('puppeteer');

(async () => {
  console.log('💤 App is sleeping. Waking it up...');

  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();

  await page.goto('https://homefinder-tampa.streamlit.app/', {
    waitUntil: 'networkidle0', // ensure complete idle
    timeout: 0,
  });

  try {
    // Optional: wait a few seconds more for delayed rendering
    await page.waitForTimeout(5000);

    // Wait and try for the button
    const buttonSelector = 'button[data-testid="wakeup-button-owner"]';

    const found = await page.waitForSelector(buttonSelector, {
      timeout: 15000,
    });

    if (found) {
      await found.click();
      console.log('✅ Clicked the wake-up button!');
    } else {
      console.log('🛑 No button found. Assuming app is already active.');
    }
  } catch (err) {
    console.log('❌ Error finding button:', err.message);
    // Debug helpers:
    await page.screenshot({ path: 'debug.png', fullPage: true });
    const html = await page.content();
    require('fs').writeFileSync('debug.html', html);
    console.log('📸 Screenshot and HTML saved for debugging.');
  }

  await browser.close();
})();
