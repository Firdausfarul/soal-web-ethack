# Writeup

For those who don't know, SVG is very similar to HTML. It can contain CSS and JavaScript code that can be used to execute XSS attacks.

The website has a registration form that has a hidden `profile_pic_url` parameter that's not available on frontend, this is our entrypoint to inject the malicious SVG. We have sanitizer and flask default protection to prevent XSS attacks. However, the sanitizer is not perfect. It only checks the url, not the content of the url / svg, so we can inject malicious code in it to steal flag cookie.

Here are the step :

1. Construct the vulnerable SVG code (see `vuln.svg`)
2. Register a new account with the SVG code as profile pic url
3. Report the new account profile page to xssbot
4. Get the flag in your webhook/server that you use on the SVG.

More detailed writeup on [this link](https://docs.google.com/document/d/1ZL95FapBvLul76OAB5y5ynIqPyUQNkkYI1uCkFrnTDI/edit?usp=sharing).
