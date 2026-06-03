import { MetadataRoute } from 'next'

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: 'Digital FTE | AI CRM Digital Factory',
    short_name: 'Digital FTE',
    description: 'The ultimate AI CRM Digital Factory for automated business workflows.',
    start_url: '/',
    display: 'standalone',
    background_color: '#000000',
    theme_color: '#000000',
    icons: [
      {
        src: '/fte.jpg',
        sizes: 'any',
        type: 'image/x-icon',
      },
    ],
  }
}
