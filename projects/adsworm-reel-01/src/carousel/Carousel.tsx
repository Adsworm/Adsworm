import {AbsoluteFill} from 'remotion';
import {Grain} from '../components/Grain';
import {sans} from '../lib/fonts';
import {AdCard} from '../reel/AdCard';
import {LogoDraw} from '../reel/LogoDraw';
import {C} from '../reel/theme';
import {Words} from '../reel/Words';

// "The 3 checks" — 4:5 carousel built from the reel's components in their settled states.
const Shell: React.FC<{n: number; children: React.ReactNode}> = ({n, children}) => (
  <AbsoluteFill style={{background: `radial-gradient(120% 70% at 50% 38%, #18181B 0%, ${C.ink} 65%)`, padding: 80, fontFamily: sans}}>
    <div style={{display: 'flex', justifyContent: 'space-between', color: C.muted, fontWeight: 600, fontSize: 28, letterSpacing: '0.16em'}}>
      <span>ADSWORM · FULL CHAIRS 01</span>
      <span>{n}/5</span>
    </div>
    <AbsoluteFill style={{top: 150, bottom: 80, left: 80, right: 80, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 44}}>
      {children}
    </AbsoluteFill>
    <Grain opacity={0.06} />
  </AbsoluteFill>
);

const Num: React.FC<{n: string}> = ({n}) => (
  <div style={{width: 96, height: 96, borderRadius: '50%', background: C.lime, color: C.ink, fontWeight: 800, fontSize: 56, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>{n}</div>
);

const Card: React.FC<{scale: number; children: React.ReactNode}> = ({scale, children}) => (
  <div style={{width: 520 * scale, height: 680 * scale}}>
    <div style={{transform: `scale(${scale})`, transformOrigin: 'top left'}}>{children}</div>
  </div>
);

export const Carousel: React.FC<{slide: number}> = ({slide}) => {
  if (slide === 1)
    return (
      <Shell n={1}>
        <Words text="3 checks before your next *clinic ad.*" size={104} at={0} set />
        <div style={{color: C.muted, fontSize: 40, fontWeight: 600, textAlign: 'center'}}>The difference between 1 clinic and 15 branches.</div>
        <div style={{padding: '14px 30px', borderRadius: 999, background: C.lime, color: C.ink, fontWeight: 800, fontSize: 34, letterSpacing: '0.08em'}}>SAVE THIS →</div>
      </Shell>
    );
  if (slide === 2)
    return (
      <Shell n={2}>
        <Num n="1" />
        <Words text="One treatment per ad." size={80} at={0} set />
        <Card scale={0.7}>
          <AdCard treatment="Hair PRP" strike={1} />
        </Card>
        <div style={{color: C.muted, fontSize: 36, textAlign: 'center', maxWidth: 740}}>Lead with the treatment, not the discount. Discounts attract price-shoppers.</div>
      </Shell>
    );
  if (slide === 3)
    return (
      <Shell n={3}>
        <Num n="2" />
        <Words text="Name the city. Name the problem." size={76} at={0} set />
        <Card scale={0.7}>
          <AdCard treatment="Hair PRP" altSubline="Hair fall after 25?" swap={1} strike={1} city={1} />
        </Card>
        <div style={{color: C.muted, fontSize: 36, textAlign: 'center', maxWidth: 740}}>Patients book the clinic that sounds like it's talking to them.</div>
      </Shell>
    );
  if (slide === 4)
    return (
      <Shell n={4}>
        <Num n="3" />
        <Words text="New creative every week." size={80} at={0} set />
        <div style={{position: 'relative', width: 900, height: 470}}>
          {[
            {w: 'W1', t: 'Hair fall after 25?', x: 40, r: -8, z: 1},
            {w: 'W3', t: 'PRP or transplant?', x: 500, r: 8, z: 1},
            {w: 'W2', t: 'Thinning crown?', x: 270, r: 0, z: 2},
          ].map((c) => (
            <div key={c.w} style={{position: 'absolute', left: c.x, top: 20, zIndex: c.z, transform: `rotate(${c.r}deg)`}}>
              <Card scale={0.62}>
                <AdCard treatment="Hair PRP" altSubline={c.t} swap={1} strike={1} city={1} week={c.w} />
              </Card>
            </div>
          ))}
        </div>
        <div style={{color: C.muted, fontSize: 36, textAlign: 'center', maxWidth: 740}}>Ad fatigue is why last month's winner stops booking.</div>
      </Shell>
    );
  return (
    <Shell n={5}>
      <LogoDraw at={-60} width={360} />
      <Words text="Want us to check *your ads?*" size={84} at={0} set maxWidth={760} />
      <div style={{padding: '22px 44px', borderRadius: 999, background: C.lime, color: C.ink, fontWeight: 800, fontSize: 48}}>Comment AUDIT</div>
      <div style={{color: C.muted, fontSize: 34, fontWeight: 600}}>Free 20-min teardown · Clinic owners only · @adsworm</div>
    </Shell>
  );
};
