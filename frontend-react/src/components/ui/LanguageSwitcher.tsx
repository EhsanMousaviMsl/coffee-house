import { useTranslation } from 'react-i18next'

export default function LanguageSwitcher() {
  const { i18n } = useTranslation()
  const currentLang = i18n.language

  const toggleLanguage = () => {
    const nextLang = currentLang === 'en' ? 'ru' : 'en'
    i18n.changeLanguage(nextLang)
  }

  return (
    <button
      onClick={toggleLanguage}
      className="text-xs tracking-wider font-sans font-semibold text-cream/50 hover:text-amber transition-all duration-300 uppercase"
      aria-label="Switch language"
    >
      {currentLang === 'en' ? 'RU' : 'EN'}
    </button>
  )
}