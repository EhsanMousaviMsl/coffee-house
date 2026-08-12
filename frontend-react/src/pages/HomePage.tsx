import { useTranslation } from 'react-i18next'
import Navbar from '../components/layout/Navbar'
import Footer from '../components/layout/Footer'
import Button from '../components/ui/Button'
import FeatureCard from '../components/ui/FeatureCard'
import MenuCard from '../components/ui/MenuCard'

export default function HomePage() {
  const { t } = useTranslation()

  return (
    <div className="bg-espresso">
      <Navbar />

      {/* ───────── HERO ───────── */}
      <section className="min-h-screen flex items-center relative overflow-hidden pt-20 pb-16">
        <div className="absolute inset-0">
          <div className="absolute top-20 left-10 w-72 h-72 rounded-full bg-amber/5 blur-3xl" />
          <div className="absolute bottom-20 right-10 w-96 h-96 rounded-full bg-amber/5 blur-3xl" />
        </div>

        <div className="max-w-6xl mx-auto px-6 w-full relative z-10">
          <div className="grid grid-cols-1 lg:grid-cols-2 items-center gap-12 lg:gap-20">
            
            {/* Left: Images */}
            <div className="relative flex justify-center">
              <div className="relative">
                <div className="w-72 h-72 lg:w-96 lg:h-96 rounded-3xl overflow-hidden border-2 border-cream/10 shadow-2xl shadow-black/40 rotate-3">
                  <img src="/bubble-tea.jpg" alt="Bubble Tea" className="w-full h-full object-cover" />
                </div>
                <div className="absolute -bottom-8 -right-8 w-48 h-48 lg:w-56 lg:h-56 rounded-2xl overflow-hidden border-2 border-amber/20 shadow-2xl shadow-black/40 -rotate-6">
                  <img src="/homePage.png" alt="Coffee" className="w-full h-full object-cover" />
                </div>
                <div className="absolute -top-4 -left-4 w-20 h-20 rounded-full bg-amber/10 flex items-center justify-center text-amber text-xs font-bold tracking-wider backdrop-blur-sm border border-amber/20">
                  ★ 4.9
                </div>
              </div>
            </div>

            {/* Right: Text */}
            <div className="text-center lg:text-left space-y-6">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-amber/20 bg-amber/5">
                <span className="w-2 h-2 rounded-full bg-amber animate-pulse" />
                <span className="text-amber text-xs tracking-wider uppercase font-medium">Open Daily 7AM – 10PM</span>
              </div>
              
              <h1 className="font-serif text-4xl lg:text-6xl font-black text-cream leading-tight">
                {t('hero.title')}
              </h1>
              
              <p className="text-cream/40 text-base lg:text-lg max-w-lg mx-auto lg:mx-0 leading-relaxed">
                {t('hero.subtitle')}
              </p>
              
              <div className="flex flex-col sm:flex-row items-center gap-4 justify-center lg:justify-start">
                <Button variant="primary">{t('hero.cta')}</Button>
                <Button variant="outline">{t('hero.secondary')}</Button>
              </div>

              <div className="flex items-center gap-8 justify-center lg:justify-start pt-4 text-cream/30 text-sm">
                <div className="text-center">
                  <span className="block text-cream text-2xl font-bold">50+</span>
                  <span>Coffee Varieties</span>
                </div>
                <div className="w-px h-10 bg-cream/10" />
                <div className="text-center">
                  <span className="block text-cream text-2xl font-bold">4.9</span>
                  <span>Avg Rating</span>
                </div>
                <div className="w-px h-10 bg-cream/10" />
                <div className="text-center">
                  <span className="block text-cream text-2xl font-bold">12</span>
                  <span>Locations</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ───────── FEATURES ───────── */}
      <section className="py-24 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-14">
            <p className="text-amber text-xs tracking-[0.2em] uppercase font-medium mb-3">{t('features.title')}</p>
            <h2 className="font-serif text-3xl lg:text-4xl font-bold text-cream">{t('features.subtitle')}</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <FeatureCard
              icon={
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4.26 10.147a60.438 60.438 0 0 0-.491 6.347A48.62 48.62 0 0 1 12 20.904a48.62 48.62 0 0 1 8.232-4.41 60.46 60.46 0 0 0-.491-6.347m-15.482 0a50.636 50.636 0 0 0-2.658-.813A59.906 59.906 0 0 1 12 3.493a59.903 59.903 0 0 1 10.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.717 50.717 0 0 1 12 13.489a50.702 50.702 0 0 1 7.74-3.342M6.75 15a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm0 0v-3.675A55.378 55.378 0 0 1 12 8.443m-7.007 11.55A5.981 5.981 0 0 0 6.75 15.75v-1.5" />
                </svg>
              }
              title={t('features.cards.beans.title')}
              description={t('features.cards.beans.description')}
            />
            <FeatureCard
              icon={
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15.362 5.214A8.252 8.252 0 0 1 12 21 8.25 8.25 0 0 1 6.038 7.047 8.287 8.287 0 0 0 9 9.601a8.983 8.983 0 0 1 3.361-6.867 8.21 8.21 0 0 0 3 2.48Z" />
                </svg>
              }
              title={t('features.cards.roasting.title')}
              description={t('features.cards.roasting.description')}
            />
            <FeatureCard
              icon={
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09Z" />
                </svg>
              }
              title={t('features.cards.baristas.title')}
              description={t('features.cards.baristas.description')}
            />
          </div>
        </div>
      </section>

      {/* ───────── MENU ───────── */}
      <section className="py-24 px-6 bg-cream/[0.01]">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-14">
            <p className="text-amber text-xs tracking-[0.2em] uppercase font-medium mb-3">{t('menu.title')}</p>
            <h2 className="font-serif text-3xl lg:text-4xl font-bold text-cream">{t('menu.subtitle')}</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-3xl mx-auto">
            <MenuCard
              name={t('menu.items.latte.name')}
              description={t('menu.items.latte.description')}
              price="$4.50"
              image="https://images.unsplash.com/photo-1570968915860-54d5c301fa9f?w=200&h=200&fit=crop"
            />
            <MenuCard
              name={t('menu.items.americano.name')}
              description={t('menu.items.americano.description')}
              price="$3.50"
              image="https://images.unsplash.com/photo-1551030173-122aabc4489c?w=200&h=200&fit=crop"
            />
            <MenuCard
              name={t('menu.items.matcha.name')}
              description={t('menu.items.matcha.description')}
              price="$5.00"
              image="https://images.unsplash.com/photo-1536256263959-770b48d82b0a?w=200&h=200&fit=crop"
            />
            <MenuCard
              name={t('menu.items.cappuccino.name')}
              description={t('menu.items.cappuccino.description')}
              price="$4.00"
              image="https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=200&h=200&fit=crop"
            />
          </div>
        </div>
      </section>

      {/* ───────── CTA ───────── */}
      <section className="py-24 px-6">
        <div className="max-w-3xl mx-auto text-center">
          <div className="bg-gradient-to-br from-coffee-brown/50 to-espresso border border-cream/10 rounded-3xl p-12 md:p-16 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-40 h-40 rounded-full bg-amber/10 blur-2xl" />
            <div className="relative z-10">
              <h2 className="font-serif text-3xl lg:text-4xl font-bold text-cream mb-4">
                {t('cta.title')}
              </h2>
              <p className="text-cream/40 text-base mb-8 max-w-md mx-auto">
                {t('cta.subtitle')}
              </p>
              <Button variant="primary">{t('cta.button')}</Button>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  )
}