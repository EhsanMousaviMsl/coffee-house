interface MenuCardProps {
  name: string
  description: string
  price: string
  image: string
}

export default function MenuCard({ name, description, price, image }: MenuCardProps) {
  return (
    <div className="group flex items-center gap-4 p-4 rounded-2xl border border-cream/5 bg-cream/[0.02] hover:bg-cream/[0.04] hover:border-amber/20 transition-all duration-500">
      <div className="w-16 h-16 rounded-xl overflow-hidden flex-shrink-0">
        <img src={image} alt={name} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700" />
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between gap-2">
          <h4 className="font-sans font-semibold text-cream text-sm">{name}</h4>
          <span className="text-amber text-sm font-bold flex-shrink-0">{price}</span>
        </div>
        <p className="text-cream/40 text-xs mt-1 leading-relaxed">{description}</p>
      </div>
    </div>
  )
}