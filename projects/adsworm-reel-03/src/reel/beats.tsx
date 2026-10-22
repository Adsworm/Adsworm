import {body, display} from '../lib/fonts';
import {ease, progress} from '../lib/motion';
import {Bars, Big, Browser, Chat, Chip, Col, CommentUI, ImageToVideo, Note, PdfCard, Row} from './receipts';
import {C} from './theme';

// Card content per section. Each builder reads `beats` (beat id → frame) so elements build the
// moment the voice says them. All facts and receipts: script/sources.md.
// `variant`: 'organic' ends on the comment-keyword UI, 'paid' (boosted post) on a plain DM card.
export type Variant = 'organic' | 'paid';
export type BeatsProps = {beats: Record<string, number>; frame: number; variant: Variant; vars: Record<string, number | string>};
const since = (beats: Record<string, number>, frame: number, id: string) => (beats[id] === undefined || frame < beats[id] ? -1 : frame - beats[id]);

// Vertically centres a single receipt in the card's content area.
const Centre: React.FC<{children: React.ReactNode}> = ({children}) => <div style={{height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center'}}>{children}</div>;

// Compact receipt line used once a full browser receipt has made its point.
const Receipt: React.FC<{t: number; text: string}> = ({t, text}) =>
  t < 0 ? null : (
    <div style={{display: 'inline-flex', alignSelf: 'flex-start', alignItems: 'center', gap: 10, padding: '8px 18px', borderRadius: 999, background: C.blueSoft, color: C.blue, fontFamily: body, fontWeight: 700, fontSize: 24, whiteSpace: 'nowrap'}}>
      <span>📄</span>
      {text}
    </div>
  );

// One of the three updates on the hook card: locked from frame 0 (the open loop), and at the
// "teeno paisa bachaate hain" beat the lock becomes a savings badge.
const LockedRow: React.FC<{n: string; text: string; unlock: number; delay: number}> = ({n, text, unlock, delay}) => {
  const u = unlock < delay ? 0 : progress(unlock, delay, 10, ease.outExpo);
  return (
    <div style={{display: 'flex', alignItems: 'center', gap: 16, padding: '10px 20px', borderRadius: 16, background: u > 0.5 ? C.greenSoft : '#F4F4F1', fontFamily: body}}>
      <div style={{width: 42, height: 42, borderRadius: '50%', background: C.blue, color: '#fff', fontFamily: display, fontSize: 30, lineHeight: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', paddingTop: 3}}>{n}</div>
      <div style={{fontWeight: 700, fontSize: 28, color: C.ink, letterSpacing: '-0.01em'}}>{text}</div>
      <div style={{marginLeft: 'auto', position: 'relative', height: 40, width: 150}}>
        <div style={{position: 'absolute', right: 0, top: 4, color: C.muted, fontSize: 26, opacity: 1 - u}}>🔒</div>
        <div style={{position: 'absolute', right: 0, top: 0, padding: '6px 14px', borderRadius: 999, background: C.green, color: '#fff', fontWeight: 800, fontSize: 22, whiteSpace: 'nowrap', opacity: u, transform: `scale(${0.8 + u * 0.2})`, transformOrigin: 'right center'}}>₹ BACHAT</div>
      </div>
    </div>
  );
};

// Paid variant end card: no Instagram chrome, one word to DM.
const DmCard: React.FC<{t: number; keyword: string}> = ({t, keyword}) => {
  if (t < 0) return null;
  const p = progress(t, 0, 14, ease.outExpo);
  const p2 = progress(t, 12, 14, ease.outExpo);
  return (
    <div style={{fontFamily: body, opacity: p, transform: `translateY(${(1 - p) * 20}px)`, display: 'flex', flexDirection: 'column', gap: 18}}>
      <div style={{fontWeight: 800, fontSize: 36, color: C.ink, lineHeight: 1.15}}>Message us one word:</div>
      <div style={{display: 'flex', alignItems: 'center', gap: 22}}>
        <div style={{padding: '22px 34px 16px', borderRadius: 24, background: C.blue, color: '#fff', fontFamily: display, fontSize: 84, lineHeight: 1, letterSpacing: '0.04em'}}>{keyword}</div>
        <div style={{opacity: p2, transform: `translateX(${(1 - p2) * -14}px)`, fontWeight: 700, fontSize: 28, lineHeight: 1.25, color: C.muted}}>
          → checklist + official links
          <br />
          in your inbox
        </div>
      </div>
    </div>
  );
};

export const BEATS: Record<string, React.FC<BeatsProps>> = {
  hook: ({beats, frame, vars}) => {
    const b = since(beats, frame, 'hook-big');
    const c = since(beats, frame, 'hook-chip');
    return (
      <Col gap={20} style={{alignItems: 'center'}}>
        <Big t={b} value={`${vars.days ?? 17} DIN`} sub="to Diwali · Lakshmi Puja, Sun 8 Nov 2026" size={150} />
        <Chip t={b} kind="ink">
          🔥 3 META UPDATES · DIWALI SE PEHLE
        </Chip>
        <div style={{width: 780, display: 'flex', flexDirection: 'column', gap: 10}}>
          <LockedRow n="1" text="Creative" unlock={c} delay={0} />
          <LockedRow n="2" text="Algorithm" unlock={c} delay={5} />
          <LockedRow n="3" text="WhatsApp" unlock={c} delay={10} />
        </div>
      </Col>
    );
  },

  one: ({beats, frame}) => {
    const r = since(beats, frame, 'one-receipt');
    const m = since(beats, frame, 'one-morph');
    return m < 0 ? (
      <Centre>
        <Browser t={r} url="facebook.com/business/news/advertising-week-new-york-2026" title="Advertising Week New York 2026: New AI Capabilities to Guide Campaigns and Reach Customers" date="6 Oct 2026 · official">
          <Note t={r} delay={18}>
            Advantage+ creative generates video from your existing static assets — now generally available.
          </Note>
        </Browser>
      </Centre>
    ) : (
      <Col gap={28} style={{alignItems: 'center'}}>
        <Receipt t={m} text="Meta for Business · Advertising Week New York · 6 Oct 2026" />
        <ImageToVideo t={m} />
        <Row gap={16}>
          <Chip t={m} delay={16} kind="green">
            ✓ Generally available
          </Chip>
          <Chip t={m} delay={22} kind="ink">
            Ads Manager → Advantage+ creative
          </Chip>
        </Row>
      </Col>
    );
  },

  two: ({beats, frame}) => {
    const r = since(beats, frame, 'two-receipt');
    const b = since(beats, frame, 'two-bars');
    const c = since(beats, frame, 'two-catch');
    const x = since(beats, frame, 'two-mix');
    return b < 0 ? (
      <Centre>
        <Browser t={r} url="engineering.fb.com/2026/10/13/ml-applications/…gem" title="Meta's Generative Ads Model (GEM): Scaling the Central Model and Compute Engine for Frontier Ads AI" date="13 Oct 2026 · official">
          <Note t={r} delay={18}>
            One central foundation model for ad delivery, replacing per-app models.
          </Note>
        </Browser>
      </Centre>
    ) : (
      <Col gap={24}>
        <Receipt t={b} text="engineering.fb.com · GEM · 13 Oct 2026 · Meta's own numbers" />
        <Bars t={b} max={25} w={870} items={[{label: 'Conversions', value: 18.9, color: C.blue}, {label: 'Click-through rate', value: 12, color: C.gold}]} />
        {c >= 0 ? (
          <Row gap={16} align="flex-start">
            <Chip t={c} kind="gold">
              ⚠ Catch
            </Chip>
            <Note t={c} delay={4} size={30}>
              “rewards a diverse mix more than repeated variations of similar assets” — Meta, 19 Oct 2026
            </Note>
          </Row>
        ) : null}
        {x >= 0 ? (
          <Row gap={14}>
            {['STATIC', 'REEL', 'CAROUSEL', 'HINGLISH'].map((k, i) => (
              <Chip key={k} t={x} delay={i * 5} kind="blue">
                {k}
              </Chip>
            ))}
          </Row>
        ) : null}
      </Col>
    );
  },

  three: ({beats, frame}) => {
    const bill = since(beats, frame, 'three-bill');
    const ch = since(beats, frame, 'three-chat');
    return (
      <Col gap={24} style={{alignItems: 'center'}}>
        <Row gap={16} align="flex-start" style={{alignSelf: 'stretch'}}>
          <Chip t={bill} kind="gold">
            1 OCT 2026
          </Chip>
          <Note t={bill} delay={4}>
            Service messages: charged after 1,000 free per month
          </Note>
        </Row>
        <Chat t={ch} brand="Your clinic · Diwali offer" adLine="Click-to-WhatsApp ad · Sponsored" reply="Diwali package ka price?" pill="Free for 7 days after your reply" w={640} />
      </Col>
    );
  },

  bonus: ({beats, frame}) => {
    const r = since(beats, frame, 'bonus-receipt');
    const b = since(beats, frame, 'bonus-bars');
    const d = since(beats, frame, 'bonus-date');
    return (
      <Col gap={22}>
        <Receipt t={r} text="Criteo India · festive 2025 · via Social Samosa, 18 Nov 2025" />
        <Note t={r} delay={4} size={32}>
          Digital ad costs, festive vs. pre-festive
        </Note>
        <Bars t={b} max={50} w={870} items={[{label: 'CPC (cost per click)', value: 45, color: C.gold}, {label: 'CPM (cost per 1,000 views)', value: 26, color: C.blue}]} />
        {d >= 0 ? (
          <Row gap={16}>
            <Chip t={d} kind="gold">
              DHANTERAS · FRI 6 NOV
            </Chip>
            <Chip t={d} delay={6} kind="blue">
              DIWALI · SUN 8 NOV
            </Chip>
          </Row>
        ) : null}
      </Col>
    );
  },

  cta: ({beats, frame, variant}) => {
    const c = since(beats, frame, 'cta-comment');
    const s = since(beats, frame, 'cta-save');
    return (
      <Col gap={22}>
        {variant === 'paid' ? <DmCard t={c} keyword="DIWALI" /> : <CommentUI t={c} name="Aman Rai" handle="@adsworm · Founder, ADSWORM" keyword="DIWALI" />}
        {s >= 0 ? (
          <Col gap={16}>
            <Row gap={14}>
              <Chip t={s} kind="ink">
                📌 SAVE
              </Chip>
              <Chip t={s} delay={5} kind="blue">
                📤 SEND TO YOUR PARTNER
              </Chip>
            </Row>
            <PdfCard t={s} title="Diwali Meta Ads Checklist" sub={variant === 'paid' ? 'Free PDF + all official links → in your inbox' : 'Free PDF + all official links → in your DM'} />
          </Col>
        ) : null}
      </Col>
    );
  },
};
