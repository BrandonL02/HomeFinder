const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  console.log('💤 Checking if app needs waking up...');

  const browser = await puppeteer.launch({ headless: false, slowMo: 50 }); // Headed mode for visibility
  const page = await browser.newPage();

  await page.goto('https://homefinder-tampa.streamlit.app/', {
    waitUntil: 'networkidle2',
    timeout: 0,
  });

  // Wait a bit extra to allow the Streamlit JS to render the button
  await page.waitForTimeout(8000);

  // Save screenshot + HTML no matter what
  const saveDebug = async () => {
    await page.screenshot({ path: 'debug.png', fullPage: true });
    const html = await page.content();
    fs.writeFileSync('debug.html', html);
    console.log('📝 Saved debug.png and debug.html');
  };

  try {
    const selector = 'button[data-testid="wakeup-button-owner"]';
    const exists = await page.$(selector);

    if (exists) {
      await exists.click();
      console.log('✅ Clicked the wake-up button!');
    } else {
      console.log('❌ Button not found! Logging HTML for analysis...');
    }

    await saveDebug();
  } catch (err) {
    console.error('❌ Error during Puppeteer execution:', err.message);
    await saveDebug();
  }

  await browser.close();
})();
