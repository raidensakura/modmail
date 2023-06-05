import React from 'react'
import { DocsThemeConfig } from 'nextra-theme-docs'

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
  project: {
    link: 'https://github.com/raidensakura/modmail',
  },
  chat: {
    link: 'https://dsc.gg/transience',
  },
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
