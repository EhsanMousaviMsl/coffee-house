import { useTranslation } from 'react-i18next'

export default function Footer() {
  const { t } = useTranslation()

  return (
    <footer className="bg-[#12221B] border-t border-cream/10 py-10 px-8 md:px-16">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-8">
        
        {/* Brand */}
        <a href="#" className="flex items-center gap-3 group cursor-pointer flex-shrink-0">
          <img src="/logo.svg" alt="Rassvet Logo" className="h-7 w-7 brightness-0 invert" />
          <span className="font-serif text-lg text-cream font-bold tracking-wide group-hover:text-amber transition-colors duration-300">
            Rassvet
          </span>
        </a>

        {/* Contact | Map | Support */}
        <div className="flex items-center gap-8 text-sm text-cream/40 font-medium">
          <a href="#" className="hover:text-cream transition-colors duration-200">
            📍 {t('footer.map')}
          </a>
          <a href="#" className="hover:text-cream transition-colors duration-200">
            📞 {t('footer.contact')}
          </a>
          <a href="#" className="hover:text-cream transition-colors duration-200">
            💬 {t('footer.support')}
          </a>
        </div>

      </div>
    </footer>
  )
}