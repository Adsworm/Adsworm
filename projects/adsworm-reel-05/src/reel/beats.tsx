import {body, display} from '../lib/fonts';
import {ease, progress} from '../lib/motion';
import {Big, Browser, Chat, Chip, Col, CommentUI, ImageToVideo, Note, PdfCard, Row} from './receipts';
import {C} from './theme';

// Card content per section. Each builder reads `beats` (beat id → frame) so elements build the
// moment the voice says them. All facts and receipts: script/sources.md.
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

// One of the three changes on the hook card: locked from frame 0 (the open loop); at "3 changes, let's go"
// the lock turns into a green tick.
const LockedRow: React.FC<{n: string; text: string; unlock: number; delay: number}> = ({n, text, unlock, delay}) => {
  const u = unlock < delay ? 0 : progress(unlock, delay, 10, ease.outExpo);
  return (
    <div style={{display: 'flex', alignItems: 'center', gap: 18, padding: '12px 22px', borderRadius: 18, background: u > 0.5 ? C.greenSoft : '#F4F4F1', fontFamily: body}}>
      <div style={{width: 48, height: 48, borderRadius: '50%', background: C.blue, color: '#fff', fontFamily: display, fontSize: 34, lineHeight: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', paddingTop: 3}}>{n}</div>
      <div style={{fontWeight: 800, fontSize: 34, color: C.ink, letterSpacing: '-0.01em'}}>{text}</div>
      <div style={{marginLeft: 'auto', position: 'relative', height: 44, width: 60}}>
        <div style={{position: 'absolute', right: 0, top: 4, color: C.muted, fontSize: 30, opacity: 1 - u}}>🔒</div>
        <div style={{position: 'absolute', right: 0, top: 0, width: 44, height: 44, borderRadius: '50%', background: C.green, color: '#fff', fontWeight: 800, fontSize: 26, display: 'flex', alignItems: 'center', justifyContent: 'center', opacity: u, transform: `scale(${0.6 + u * 0.4})`}}>✓</div>
      </div>
    </div>
  );
};

export const BEATS: Record<string, React.FC<BeatsProps>> = {
  hook: ({beats, frame, vars}) => {
    const b = since(beats, frame, 'hook-big');
    const c = since(beats, frame, 'hook-chip');
    return (
      <Col gap={22} style={{alignItems: 'center'}}>
        <Big t={b} value={`${vars.days ?? 36} DAYS`} sub="to Black Friday · Fri 27 Nov 2026" size={160} />
        <Chip t={b} kind="ink">
          3 META CHANGES · WHAT YOU PAY FOR ADS
        </Chip>
        <div style={{width: 820, display: 'flex', flexDirection: 'column', gap: 10}}>
          <LockedRow n="1" text="Photo → video ads" unlock={c} delay={0} />
          <LockedRow n="2" text="Meta's new ad AI" unlock={c} delay={5} />
          <LockedRow n="3" text="WhatsApp pricing" unlock={c} delay={10} />
        </div>
      </Col>
    );
  },

  one: ({beats, frame}) => {
    const r = since(beats, frame, 'one-receipt');
    const m = since(beats, frame, 'one-morph');
    return m < 0 ? (
      <Centre>
        <Browser t={r} url="facebook.com/business/news/advertising-week-new-york-2026" title="New AI Capabilities to Guide Campaigns and Reach Customers" date="6 Oct 2026 · official">
          <Note t={r} delay={18}>
            Advantage+ creative makes a video from your existing photos. Now available to everyone.
          </Note>
        </Browser>
      </Centre>
    ) : (
      <Col gap={28} style={{alignItems: 'center'}}>
        <Receipt t={m} text="Meta for Business · 6 Oct 2026" />
        <ImageToVideo t={m} />
        <Row gap={16}>
          <Chip t={m} delay={16} kind="green">
            ✓ No shoot needed
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
    const x = since(beats, frame, 'two-mix');
    return b < 0 ? (
      <Centre>
        <Browser t={r} url="engineering.fb.com/2026/10/13/ml-applications/…gem" title="Meta's Generative Ads Model (GEM)" date="13 Oct 2026 · official">
          <Note t={r} delay={18}>
            One central AI model now decides who sees which ad, across Meta's apps.
          </Note>
        </Browser>
      </Centre>
    ) : (
      <Col gap={22} style={{alignItems: 'center'}}>
        <Receipt t={b} text="engineering.fb.com · 13 Oct 2026 · Meta's own numbers" />
        <Big t={b} value="+18.9%" sub="more conversions (a sale or a lead)" color={C.green} size={x >= 0 ? 130 : 170} />
        {x < 0 ? (
          <Chip t={b} delay={14} kind="blue">
            + 12% more clicks
          </Chip>
        ) : (
          <Col gap={16} style={{alignItems: 'center'}}>
            <Row gap={14}>
              <Chip t={x} kind="gold">
                ✕ 10 copies of 1 ad
              </Chip>
              <Chip t={x} delay={6} kind="green">
                ✓ Different ads win
              </Chip>
            </Row>
            <Row gap={12}>
              {['PHOTO', 'VIDEO', 'CAROUSEL'].map((k, i) => (
                <Chip key={k} t={x} delay={12 + i * 5} kind="blue">
                  {k}
                </Chip>
              ))}
            </Row>
          </Col>
        )}
      </Col>
    );
  },

  three: ({beats, frame}) => {
    const bill = since(beats, frame, 'three-bill');
    const ch = since(beats, frame, 'three-chat');
    return ch < 0 ? (
      <Col gap={22} style={{alignItems: 'center'}}>
        <Chip t={bill} kind="gold">
          FROM 1 OCT 2026
        </Chip>
        <Big t={bill} value="1,000" sub="free replies a month, then you pay per message" size={180} />
      </Col>
    ) : (
      <Col gap={22} style={{alignItems: 'center'}}>
        <Receipt t={ch} text="1,000 free replies / month · then paid" />
        <Chat t={ch} brand="Your brand · from your ad" adLine="Click-to-WhatsApp ad · Sponsored" reply="Is this still available?" pill="Free for up to 7 days" w={640} />
      </Col>
    );
  },

  cta: ({beats, frame}) => {
    const c = since(beats, frame, 'cta-comment');
    const s = since(beats, frame, 'cta-save');
    return (
      <Col gap={22}>
        <CommentUI t={c} name="Aman Rai" handle="@amanrai.official · Founder, ADSWORM" keyword="META" />
        {s >= 0 ? (
          <Col gap={16}>
            <Row gap={14}>
              <Chip t={s} kind="ink">
                📌 SAVE
              </Chip>
              <Chip t={s} delay={5} kind="blue">
                📤 SEND TO A FOUNDER
              </Chip>
            </Row>
            <PdfCard t={s} title="Meta Q4 Ads Checklist" sub="Free PDF + all official links → in your DM" />
          </Col>
        ) : null}
      </Col>
    );
  },
};
