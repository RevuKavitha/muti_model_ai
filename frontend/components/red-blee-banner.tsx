import Image from "next/image";

interface Props {
  subtitle?: string;
}

export function RedBleeBanner({ subtitle = "Mission Control Active" }: Props) {
  return (
    <section className="banner-enter mb-8 rounded-2xl border border-border bg-black/40 p-4 sm:p-5">
      <div className="flex flex-wrap items-center gap-4">
        <div className="mascot-glow mascot-pulse grid h-32 w-32 place-items-center rounded-3xl border border-red-500/60 bg-black/80">
          <div className="relative h-full w-full overflow-hidden rounded-[inherit]">
            <Image
              src="/mascot-tiger.png"
              alt="Red Blee mascot"
              fill
              sizes="128px"
              className="object-cover scale-110 contrast-110 saturate-110"
              priority
            />
            <span className="scanline-overlay" aria-hidden="true" />
          </div>
        </div>

        <div>
          <h1 className="font-display text-4xl leading-none sm:text-5xl">
            <span className="title-sheen text-white">RED </span>
            <span className="text-red-500">BLEE</span>
          </h1>
          <p className="mt-2 flex items-center gap-2 text-xs uppercase tracking-[0.32em] text-gray-400">
            <span className="status-pulse h-2.5 w-2.5 rounded-full bg-emerald-400 shadow-[0_0_18px_rgba(52,211,153,0.75)]" />
            {subtitle}
          </p>
        </div>
      </div>
    </section>
  );
}
