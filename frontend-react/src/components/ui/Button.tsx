interface ButtonProps {
  children: React.ReactNode
  variant?: 'primary' | 'outline'
  className?: string
}

export default function Button({ children, variant = 'primary', className = '' }: ButtonProps) {
  const base = "inline-block px-8 py-3 rounded-full font-sans font-semibold text-lg tracking-wide transition-all duration-300 transform hover:scale-105 shadow-md"
  
  const variants = {
    primary: "bg-amber text-espresso hover:bg-amber-dark",
    outline: "border-2 border-cream/30 text-cream hover:bg-cream/10"
  }

  return (
    <button className={`${base} ${variants[variant]} ${className}`}>
      {children}
    </button>
  )
}