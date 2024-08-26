import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: 'binks.py docs',
			social: {
				github: 'https://github.com/jmhayes3/binks.py',
			},
			sidebar: [
				// A single link item labelled “Home”.
				{ label: 'Home', link: '/' },
				// A group labelled “Start Here” containing four links.
				{
					label: 'Getting Started',
					items: [
						// Using `slug` for internal links.
						{ slug: 'intro' },
						{ slug: 'installation' },
						// Or using the shorthand for internal links.
						'tutorial',
						'next-steps',
					],
					label: 'Commands',
					items: [
						// Using `slug` for internal links.
						{ label: 'version', link: '/commands/version' },
						{ label: 'chat', link: '/commands/chat' },
					],
				},
				// A group linking to all pages in the reference directory.
				{
					label: 'Reference',
					autogenerate: { directory: 'reference' },
				},
			],
		}),
	],
});
