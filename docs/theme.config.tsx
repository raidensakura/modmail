import React from 'react'
import { DocsThemeConfig } from 'nextra-theme-docs'
import { useConfig } from 'nextra-theme-docs'
import { useRouter } from 'next/router'

// base64 encoding that supports unicode strings
function base64Encode(str) {
	const buffer = Buffer.from(str, 'utf-8')
	return buffer.toString('base64')
}

const config: DocsThemeConfig = {
  logo: <>
    <img
      src="/logo-ico.png"
      style={{ height: 20, objectFit: 'contain' }}
      alt="zeabur"
      className="black-logo"
    />
    <img
      src="/logo-long.png"
      style={{ height: 20, objectFit: 'contain' }}
      alt="zeabur"
      className="white-logo"
    />
  </>,
  useNextSeoProps() {
    return {
      titleTemplate: 'Modmail - %s',
    }
  },
  head: () => {
    const { frontMatter } = useConfig();

    return <>
      <meta name="description" content="Modmail Docs" />
      <link
        rel="apple-touch-icon"
        sizes="180x180"
        href="/favicon.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="192x192"
        href="/favicon.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="32x32"
        href="/favicon.png"
      />
      <link
        rel="icon"
        type="image/png"
        sizes="16x16"
        href="/favicon.png"
      />
    </>;
  },
  project: {
    link: 'https://github.com/raidensakura/modmail',
  },
  sidebar: {
    defaultMenuCollapseLevel: 1,
  },
  chat: {
    link: 'https://dsc.gg/transience',
  },
  primaryHue: { dark: 278, light: 265 },
  docsRepositoryBase: 'https://github.com/raidensakura/modmail/tree/develop/docs',
  footer: {
    text: (
      <span>
        {new Date().getFullYear()} ©{' '}
        <a href="https://github.com/raidensakura/modmail" target="_blank">
          A fork of Modmail
        </a>
        .
      </span>
    ),
  },
}

export default config
