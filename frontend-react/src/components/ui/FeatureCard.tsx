interface FeatureCardProps {
  icon: React.ReactNode
  title: string
  description: string
}

export default function FeatureCard({ icon, title, description }: FeatureCardProps) {
  return (
    <div className="group text-center p-8 rounded-2xl border border-cream/5 bg-cream/[0.02] hover:bg-cream/[0.04] hover:border-amber/20 transition-all duration-500">
      <div className="w-14 h-14 mx-auto mb-5 rounded-xl bg-amber/10 flex items-center justify-center text-amber group-hover:scale-110 transition-transform duration-500">
        {icon}
      </div>
      <h3 className="font-serif text-xl text-cream font-bold mb-3">{title}</h3>
      <p className="text-cream/40 text-sm leading-relaxed">{description}</p>
    </div>
  )
}