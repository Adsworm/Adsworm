import {body, display} from '../lib/fonts';
import {ease, progress} from '../lib/motion';
import {Bars, Big, Browser, Chart, Chat, Chip, Col, CommentUI, ImageToVideo, Note, PdfCard, Phone, Ring, Row} from './receipts';
import {C} from './theme';
import {Checks, Deadline, Follow, HookPrice, InApp, PauseButton, Shop, Split, Stat, Sticker, Versus, type Tone} from './board';

// Data-driven card content: script.json → sections[].views. A view takes over the card at its `at` beat
// (a line's beat id) and stays until the next view; each item can wait for its own `at` beat. This is
// what the director agent writes, so a new reel needs no hand-written TSX.
type Kind = 'blue' | 'green' | 'gold' | 'ink';
export type Item =
  | {type: 'big'; value: string; sub?: string; color?: keyof typeof C; size?: number; at?: string}
  | {type: 'chip'; text: string; kind?: Kind; delay?: number; at?: string}
  | {type: 'chips'; items: string[]; kind?: Kind; delay?: number; at?: string}
  | {type: 'browser'; url: string; title: string; date?: string; note?: string; at?: string}
  | {type: 'note'; text: string; size?: number; at?: string}
  | {type: 'receipt'; text: string; at?: string}
  | {type: 'bars'; items: {label: string; value: number; color?: keyof typeof C}[]; max?: number; at?: string}
  | {type: 'chart'; points: [number, number][]; title?: string; note?: string; at?: string}
  | {type: 'ring'; value: string; sub: string; at?: string}
  | {type: 'chat'; brand: string; adLine: string; reply: string; pill: string; at?: string}
  | {type: 'phone'; label?: string; adTitle?: string; cta?: string; at?: string}
  | {type: 'imageToVideo'; at?: string}
  | {type: 'comment'; keyword: string; name?: string; handle?: string; at?: string}
  | {type: 'pdf'; title: string; sub: string; label?: string; at?: string}
  | {type: 'checklist'; rows: string[]; unlockAt?: string; at?: string}
  | {type: 'steps'; items: string[]; stagger?: number; at?: string}
  | {type: 'compare'; bad: {title: string; lines: string[]}; good: {title: string; lines: string[]}; goodAt?: string; goodWord?: string; at?: string; word?: string}
  | {type: 'hookPrice'; smileWord: string; at?: string; word?: string}
  | {type: 'stat'; value: number; prefix?: string; suffix?: string; label: string; color?: Tone; arrow?: 'up' | 'down'; at?: string; word?: string}
  | {type: 'versus'; left: {value: number; prefix?: string; suffix?: string; label: string; color?: Tone; arrow?: 'up' | 'down'}; right: {value: number; prefix?: string; suffix?: string; label: string; color?: Tone; arrow?: 'up' | 'down'}; qAt?: string; at?: string; word?: string}
  | {type: 'pauseButton'; text: string; strikeAt: string; at?: string; word?: string}
  | {type: 'shop'; rentWord: string; buyWord: string; chip: string; at?: string; word?: string}
  | {type: 'sticker'; text: string; color?: Tone; x: number; y: number; rotate?: number; at?: string; word?: string}
  | {type: 'checks'; items: {text: string; word: string}[]; at?: string; word?: string}
  | {type: 'follow'; share: string; at?: string; word?: string}
  | {type: 'inApp'; tapWord: string; webWord: string; at?: string; word?: string}
  | {type: 'deadline'; month: string; day: string; note: string; at?: string; word?: string}
  | {type: 'split'; left: {emoji: string; label: string}; right: {emoji: string; label: string}; at?: string; word?: string};
export type View = {at: string; word?: string; items: Item[]; align?: 'center' | 'top'};

const since = (beats: Record<string, number>, frame: number, id?: string) => (id === undefined || beats[id] === undefined || frame < beats[id] ? -1 : frame - beats[id]);
export type WordClock = (word: string) => number; // frames since `word` is spoken in this view (−1 before)
const fill = (s: string, vars: Record<string, number | string>) => s.replace(/\{(\w+)\}/g, (_, k) => String(vars[k] ?? `{${k}}`));

const Receipt: React.FC<{t: number; text: string}> = ({t, text}) =>
  t < 0 ? null : (
    <div style={{display: 'inline-flex', alignSelf: 'center', alignItems: 'center', gap: 10, padding: '8px 18px', borderRadius: 999, background: C.blueSoft, color: C.blue, fontFamily: body, fontWeight: 700, fontSize: 24, whiteSpace: 'nowrap', opacity: progress(t, 0, 10)}}>
      <span>📄</span>
      {text}
    </div>
  );

// Rows locked from the view's start; at `unlockAt` each lock turns into a green tick (open loop → payoff).
const Checklist: React.FC<{t: number; rows: string[]; unlock: number}> = ({t, rows, unlock}) => (
  <div style={{width: 840, display: 'flex', flexDirection: 'column', gap: 10, opacity: progress(t, 0, 12)}}>
    {rows.map((text, i) => {
      const u = unlock < i * 5 ? 0 : progress(unlock, i * 5, 10, ease.outExpo);
      return (
        <div key={i} style={{display: 'flex', alignItems: 'center', gap: 18, padding: '12px 22px', borderRadius: 18, background: u > 0.5 ? C.greenSoft : '#F4F4F1', fontFamily: body}}>
          <div style={{width: 48, height: 48, borderRadius: '50%', background: C.blue, color: '#fff', fontFamily: display, fontSize: 34, lineHeight: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', paddingTop: 3}}>{i + 1}</div>
          <div style={{fontWeight: 800, fontSize: 34, color: C.ink, letterSpacing: '-0.01em'}}>{text}</div>
          <div style={{marginLeft: 'auto', position: 'relative', height: 44, width: 44}}>
            <div style={{position: 'absolute', right: 0, top: 4, fontSize: 30, opacity: 1 - u}}>🔒</div>
            <div style={{position: 'absolute', inset: 0, borderRadius: '50%', background: C.green, color: '#fff', fontWeight: 800, fontSize: 26, display: 'flex', alignItems: 'center', justifyContent: 'center', opacity: u, transform: `scale(${0.6 + u * 0.4})`}}>✓</div>
          </div>
        </div>
      );
    })}
  </div>
);

// Numbered steps that land one by one — the "here's the fix" view.
const Steps: React.FC<{t: number; items: string[]; stagger: number}> = ({t, items, stagger}) => (
  <div style={{width: 860, display: 'flex', flexDirection: 'column', gap: 14}}>
    {items.map((text, i) => {
      const p = progress(t, i * stagger, 12, ease.outExpo);
      return t < i * stagger ? null : (
        <div key={i} style={{display: 'flex', alignItems: 'center', gap: 20, padding: '16px 24px', borderRadius: 20, background: '#F4F4F1', fontFamily: body, opacity: p, transform: `translateX(${(1 - p) * -30}px)`}}>
          <div style={{width: 54, height: 54, flex: 'none', borderRadius: 16, background: C.blue, color: '#fff', fontFamily: display, fontSize: 38, display: 'flex', alignItems: 'center', justifyContent: 'center', paddingTop: 3}}>{i + 1}</div>
          <div style={{fontWeight: 800, fontSize: 34, lineHeight: 1.15, color: C.ink, letterSpacing: '-0.01em'}}>{text}</div>
        </div>
      );
    })}
  </div>
);

// ✕ what most people do  vs  ✓ what works — the clearest "before/after" for a non-marketer.
const Compare: React.FC<{t: number; good: number; bad: {title: string; lines: string[]}; ok: {title: string; lines: string[]}}> = ({t, good, bad, ok}) => {
  const col = (side: {title: string; lines: string[]}, isGood: boolean, tt: number) => {
    const p = progress(tt, 0, 14, ease.outExpo);
    return (
      <div style={{flex: 1, borderRadius: 26, padding: '24px 24px 26px', background: isGood ? C.greenSoft : '#FBEDEC', border: `3px solid ${isGood ? C.green : C.red}`, fontFamily: body, opacity: tt < 0 ? 0.15 : p, transform: `translateY(${(1 - (tt < 0 ? 0 : p)) * 24}px)`}}>
        <div style={{fontWeight: 800, fontSize: 40, color: isGood ? C.green : C.red, marginBottom: 14}}>{isGood ? '✓ ' : '✕ '}{side.title}</div>
        {side.lines.map((l, i) => (
          <div key={i} style={{fontWeight: 700, fontSize: 38, lineHeight: 1.2, color: C.ink, marginTop: 10, opacity: tt < i * 6 ? 0 : progress(tt, i * 6, 10)}}>{l}</div>
        ))}
      </div>
    );
  };
  return (
    <div style={{width: 870, display: 'flex', gap: 20}}>
      {col(bad, false, t)}
      {col(ok, true, good)}
    </div>
  );
};

const ItemView: React.FC<{item: Item; t: number; beats: Record<string, number>; frame: number; vars: Record<string, number | string>; wc: WordClock}> = ({item, t, beats, frame, vars, wc}) => {
  const f = (s: string) => fill(s, vars);
  switch (item.type) {
    case 'big':
      return <Big t={t} value={f(item.value)} sub={item.sub ? f(item.sub) : undefined} color={item.color ? C[item.color] : undefined} size={item.size ?? 170} />;
    case 'chip':
      return (
        <Chip t={t} delay={item.delay} kind={item.kind}>
          {f(item.text)}
        </Chip>
      );
    case 'chips':
      return (
        <Row gap={12} style={{flexWrap: 'wrap', justifyContent: 'center', maxWidth: 880}}>
          {item.items.map((k, i) => (
            <Chip key={k} t={t} delay={(item.delay ?? 0) + i * 5} kind={item.kind}>
              {f(k)}
            </Chip>
          ))}
        </Row>
      );
    case 'browser':
      return (
        <Browser t={t} url={item.url} title={f(item.title)} date={item.date}>
          {item.note ? (
            <Note t={t} delay={18}>
              {f(item.note)}
            </Note>
          ) : null}
        </Browser>
      );
    case 'note':
      return (
        <Note t={t} size={item.size}>
          {f(item.text)}
        </Note>
      );
    case 'receipt':
      return <Receipt t={t} text={f(item.text)} />;
    case 'bars':
      return <Bars t={t} items={item.items.map((b) => ({...b, color: b.color ? C[b.color] : undefined}))} max={item.max} w={860} />;
    case 'chart':
      return <Chart t={t} points={item.points} title={item.title} note={item.note} w={860} h={280} />;
    case 'ring':
      return <Ring t={t} value={f(item.value)} sub={f(item.sub)} />;
    case 'chat':
      return <Chat t={t} brand={item.brand} adLine={item.adLine} reply={item.reply} pill={item.pill} w={640} />;
    case 'phone':
      return <Phone t={t} label={item.label} adTitle={item.adTitle} cta={item.cta} width={196} />;
    case 'imageToVideo':
      return <ImageToVideo t={t} />;
    case 'comment':
      return <CommentUI t={t} name={item.name ?? 'ADSWORM'} handle={item.handle ?? '@adsworm · Performance marketing agency'} keyword={item.keyword} />;
    case 'pdf':
      return <PdfCard t={t} title={f(item.title)} sub={f(item.sub)} label={item.label} />;
    case 'checklist':
      return <Checklist t={t} rows={item.rows.map(f)} unlock={since(beats, frame, item.unlockAt)} />;
    case 'steps':
      return <Steps t={t} items={item.items.map(f)} stagger={item.stagger ?? 10} />;
    case 'compare':
      return <Compare t={t} good={item.goodWord ? wc(item.goodWord) : item.goodAt ? since(beats, frame, item.goodAt) : t - 12} bad={item.bad} ok={item.good} />;
    case 'hookPrice':
      return <HookPrice t={t} smileT={wc(item.smileWord)} />;
    case 'stat':
      return <Stat t={t} value={item.value} prefix={item.prefix} suffix={item.suffix} label={item.label} color={item.color} arrow={item.arrow} />;
    case 'versus':
      return <Versus t={t} qT={item.qAt ? since(beats, frame, item.qAt) : -1} left={item.left} right={item.right} />;
    case 'pauseButton':
      return <PauseButton t={t} strikeT={since(beats, frame, item.strikeAt)} text={item.text} />;
    case 'shop':
      return <Shop t={t} rentT={wc(item.rentWord)} buyT={wc(item.buyWord)} chip={item.chip} />;
    case 'sticker':
      return <Sticker t={t} text={f(item.text)} color={item.color} x={item.x} y={item.y} rotate={item.rotate} />;
    case 'checks':
      return <Checks t={t} items={item.items.map((c) => ({text: f(c.text), at: wc(c.word)}))} />;
    case 'follow':
      return <Follow t={t} share={f(item.share)} />;
    case 'inApp':
      return <InApp t={t} tapT={wc(item.tapWord)} webT={wc(item.webWord)} />;
    case 'deadline':
      return <Deadline t={t} month={item.month} day={item.day} note={f(item.note)} />;
    case 'split':
      return <Split t={t} left={item.left} right={item.right} />;
  }
};

const norm = (w: string) => w.toLowerCase().replace(/[^a-z0-9%]/g, '');

const ViewBody: React.FC<{v: View; idx: number; vt: number; beats: Record<string, number>; frame: number; vars: Record<string, number | string>; wc: WordClock}> = ({v, idx, vt, beats, frame, vars, wc}) => {
  const flow = v.items.filter((i) => i.type !== 'sticker');
  const stickers = v.items.filter((i) => i.type === 'sticker');
  const only = flow.length === 1 && flow[0].type === 'browser';
  const tOf = (item: Item) => ('word' in item && item.word ? wc(item.word) : item.at ? since(beats, frame, item.at) : vt);
  return (
    <div style={{position: 'relative', height: '100%'}}>
      <Col gap={22} style={{alignItems: 'center', height: '100%', justifyContent: only || v.align !== 'top' ? 'center' : 'flex-start'}}>
        {flow.map((item, i) => {
          const t = tOf(item);
          return t < 0 && item.type !== 'compare' ? null : <ItemView key={`${idx}-${i}`} item={item} t={t} beats={beats} frame={frame} vars={vars} wc={wc} />;
        })}
      </Col>
      {stickers.map((item, i) => <ItemView key={`s${idx}-${i}`} item={item} t={tOf(item)} beats={beats} frame={frame} vars={vars} wc={wc} />)}
    </div>
  );
};

type Spoken = {t: number; w: string}[];
export const Views: React.FC<{views: View[]; beats: Record<string, number>; frame: number; vars: Record<string, number | string>; words?: Spoken; fps?: number}> = ({views, beats, frame, vars, words = [], fps = 30}) => {
  // a view starts at its beat, or at a word spoken after that beat (`word`)
  const norm0 = (w: string) => w.toLowerCase().replace(/[^a-z0-9%]/g, '');
  const startOf = (v: View) => {
    const b = beats[v.at];
    if (b === undefined) return Infinity;
    if (!v.word) return b;
    const hit = words.find((w) => w.t * fps >= b - 2 && norm0(w.w).startsWith(norm0(v.word!)));
    return hit ? Math.round(hit.t * fps) : b;
  };
  const active = views.reduce((acc, v, i) => (frame >= startOf(v) ? i : acc), 0);
  const v = views[active];
  if (!v) return null;
  const vt = Math.max(frame - startOf(v), active === 0 ? 0 : -1);
  const from = startOf(v) / fps;
  const wc: WordClock = (word) => {
    const hit = words.find((w) => w.t >= from - 0.05 && norm(w.w).startsWith(norm(word)));
    return hit && frame >= Math.round(hit.t * fps) ? frame - Math.round(hit.t * fps) : -1;
  };
  // outgoing view slides up and fades while the new one rises in (10 frames)
  const prev = active > 0 && vt < 10 ? views[active - 1] : null;
  const k = Math.min(1, vt / 10);
  return (
    <div style={{position: 'relative', height: '100%'}}>
      {prev ? (
        <div style={{position: 'absolute', inset: 0, opacity: 1 - k, transform: `translateY(${-k * 80}px) scale(${1 - 0.06 * k})`}}>
          <ViewBody v={prev} idx={active - 1} vt={vt + 999} beats={beats} frame={frame} vars={vars} wc={() => 999} />
        </div>
      ) : null}
      <div style={{position: 'absolute', inset: 0, opacity: prev ? k : 1, transform: prev ? `translateY(${(1 - k) * 90}px)` : undefined}}>
        <ViewBody v={v} idx={active} vt={vt} beats={beats} frame={frame} vars={vars} wc={wc} />
      </div>
    </div>
  );
};
