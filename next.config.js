// next.config.js
module.exports = (async () => {
  const nextraModule = await import('nextra')
  const nextra = nextraModule.default || nextraModule
  const withNextra = nextra({
    theme: 'nextra-theme-docs',
    themeConfig: './theme.config.jsx',
  })
  // withNextra is a function that returns the Next config
  return withNextra()
})()
