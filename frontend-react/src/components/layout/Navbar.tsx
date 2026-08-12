import { useState, useRef, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import LanguageSwitcher from '../ui/LanguageSwitcher'

export default function Navbar() {
  const { t } = useTranslation()
  const [dropdownOpen, setDropdownOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setDropdownOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const navLinks = [t('nav.home'), t('nav.menu'), t('nav.aboutUs')]

  return (
    <header className="fixed top-0 left-0 right-0 z-50 h-20 flex items-center px-8 md:px-16 bg-espresso border-b border-cream/10">
      <div className="w-full max-w-7xl mx-auto flex items-center justify-between">
        
        {/* LEFT: Logo */}
        <a href="#" className="flex items-center gap-3 group cursor-pointer flex-shrink-0">
          <img src="/logo.svg" alt="Rassvet Logo" className="h-9 w-9 brightness-0 invert transition-transform duration-300 group-hover:scale-110" />
          <span className="font-serif text-lg text-cream font-bold tracking-wide group-hover:text-amber transition-colors duration-300">
            Rassvet
          </span>
        </a>

        {/* CENTER: Nav Links */}
        <nav className="hidden md:flex items-center space-x-8 text-sm tracking-wider font-medium">
          {navLinks.map((link) => (
            <a
              key={link}
              href="#"
              className="text-cream/60 hover:text-cream transition-all duration-300"
            >
              {link}
            </a>
          ))}
        </nav>

        {/* RIGHT: Language + Social + Login */}
        <div className="flex items-center space-x-4 flex-shrink-0">
          <LanguageSwitcher />

          <a href="https://t.me/yourusername" target="_blank" rel="noopener noreferrer" className="text-cream/40 hover:text-amber transition-colors duration-300">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221l-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.446 1.394c-.14.18-.357.295-.6.295-.002 0-.003 0-.005 0l.213-3.054 5.56-5.022c.24-.213-.054-.334-.373-.121l-6.869 4.326-2.96-.924c-.64-.203-.658-.64.135-.954l11.566-4.458c.538-.196 1.006.128.832.938z"/>
            </svg>
          </a>

          <a href="https://instagram.com/yourusername" target="_blank" rel="noopener noreferrer" className="text-cream/40 hover:text-amber transition-colors duration-300">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
            </svg>
          </a>

          {/* Login Dropdown */}
          <div className="relative" ref={dropdownRef}>
            <button
              onClick={() => setDropdownOpen(!dropdownOpen)}
              className="w-8 h-8 rounded-full border border-cream/20 flex items-center justify-center text-cream/40 hover:text-amber hover:border-amber/40 transition-all duration-300"
              aria-label="User menu"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </button>
            <div
              className={`absolute right-0 mt-3 w-44 bg-coffee-brown border border-cream/10 rounded-xl shadow-2xl shadow-black/30 overflow-hidden transition-all duration-200 origin-top-right ${
                dropdownOpen ? 'opacity-100 scale-100 visible' : 'opacity-0 scale-95 invisible'
              }`}
            >
              <a href="#" className="block px-4 py-3 text-sm text-cream/70 hover:text-cream hover:bg-cream/5 transition-colors duration-200" onClick={() => setDropdownOpen(false)}>
                {t('nav.signIn')}
              </a>
              <a href="#" className="block px-4 py-3 text-sm text-cream/70 hover:text-cream hover:bg-cream/5 transition-colors duration-200 border-t border-cream/5" onClick={() => setDropdownOpen(false)}>
                {t('nav.createAccount')}
              </a>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}