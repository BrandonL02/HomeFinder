const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: "new",  // or true
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.goto('https://homefinder-tampa.streamlit.app/', {
    waitUntil: 'networkidle2',
    timeout: 0
  });

  // Wait for the iframe to be available
  const iframeElementHandle = await page.waitForSelector('iframe', { timeout: 10000 });
  const iframe = await iframeElementHandle.contentFrame();

  if (!iframe) {
    console.log('Could not get iframe content.');
    await browser.close();
    return;
  }

  try {
    await iframe.waitForSelector('button', { timeout: 10000 });

    const buttonText = await iframe.evaluate(() => {
      const button = document.querySelector('button');
      return button?.innerText || '';
    });

    if (buttonText.includes('Yes, get this app back up!')) {
      await iframe.click('button');
      console.log('Wake up button clicked!');
    } else {
      console.log('No wake-up button found; app is already up.');
    }
  } catch (err) {
    console.log('No button found or page is already up.');
  }

  await browser.close();
})();
