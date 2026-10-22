import {body} from '../lib/fonts';
import {Bars, Big, Browser, Chart, Chat, Chip, Col, CommentUI, ImageToVideo, Note, PdfCard, Row} from './receipts';
import {C} from './theme';

// Card content per section. Each builder reads `beats` (beat id → frame) so elements build the
// moment the voice says them. All facts and receipts: script/sources.md.
export type BeatsProps = {beats: Record<string, number>; frame: number};
const since = (beats: Record<string, number>, frame: number, id: string) => (beats[id] === undefined || frame < beats[id] ? -1 : frame - beats[id]);

// Compact receipt line used once a full browser receipt has made its point.
const Receipt: React.FC<{t: number; text: string}> = ({t, text}) =>
  t < 0 ? null : (
    <div style={{display: 'inline-flex', alignItems: 'center', gap: 10, padding: '8px 16px', borderRadius: 999, background: C.blueSoft, color: C.blue, fontFamily: body, fontWeight: 700, fontSize: 22}}>
      <span>📄</span>
      {text}
    </div>
  );

const DateTile: React.FC<{t: number; delay: number; label: string; value: string; hot?: boolean}> = ({t, delay, label, value, hot}) => {
  if (t < delay) return null;
  const p = Math.min(1, (t - delay) / 10);
  return (
    <div style={{width: 250, padding: '16px 0 14px', borderRadius: 18, border: `2px solid ${hot ? C.blue : C.line}`, background: hot ? C.blueSoft : '#fff', textAlign: 'center', fontFamily: body, opacity: p, transform: `translateY(${(1 - p) * 14}px)`}}>
      <div style={{fontSize: 20, fontWeight: 800, letterSpacing: '0.12em', color: hot ? C.blue : C.muted}}>{label}</div>
      <div style={{fontSize: 30, fontWeight: 800, color: C.ink, marginTop: 4}}>{value}</div>
    </div>
  );
};

export const BEATS: Record<string, React.FC<BeatsProps>> = {
  hook: ({beats, frame}) => (
    <Col gap={34} style={{alignItems: 'center', paddingTop: 70}}>
      <Big t={since(beats, frame, 'hook-big')} value="17 DIN" sub="to Diwali · Lakshmi Puja, Sun 8 Nov 2026" />
      <Chip t={since(beats, frame, 'hook-chip')} kind="ink">
        🔥 3 META UPDATES · DIWALI SE PEHLE
      </Chip>
      <Row gap={14} style={{marginTop: 30}}>
        {[['DHANTERAS', 'Fri 6 Nov'], ['DIWALI', 'Sun 8 Nov'], ['BHAI DOOJ', 'Wed 11 Nov']].map(([k, v], i) => (
          <DateTile key={k} t={since(beats, frame, 'hook-chip')} delay={6 + i * 5} label={k} value={v} hot={i === 1} />
        ))}
      </Row>
    </Col>
  ),

  one: ({beats, frame}) => {
    const r = since(beats, frame, 'one-receipt');
    const m = since(beats, frame, 'one-morph');
    const s = since(beats, frame, 'one-stat');
    return m < 0 ? (
      <Browser t={r} url="facebook.com/business/news/advertising-week-new-york-2026" title="Advertising Week New York 2026: New AI Capabilities to Guide Campaigns and Reach Customers" date="6 Oct 2026 · official">
        <Note t={r} delay={18} size={28}>
          Advantage+ creative: video generated from your existing static assets — now generally available.
        </Note>
      </Browser>
    ) : (
      <Col gap={26} style={{alignItems: 'center'}}>
        <Receipt t={m} text="Meta for Business · Advertising Week New York · 6 Oct 2026" />
        <ImageToVideo t={m} />
        <Row gap={16}>
          <Chip t={m} delay={20} kind="green">
            ✓ Generally available
          </Chip>
          <Chip t={s} kind="ink">
            60% of time on FB + IG = video (Meta)
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
      <Browser t={r} url="engineering.fb.com/2026/10/13/ml-applications/…gem" title="Meta's Generative Ads Model (GEM): Scaling the Central Model and Compute Engine for Frontier Ads AI" date="13 Oct 2026 · official">
        <Note t={r} delay={18} size={28}>
          One central foundation model for ad delivery, replacing per-app models.
        </Note>
      </Browser>
    ) : (
      <Col gap={26}>
        <Receipt t={b} text="engineering.fb.com · GEM · 13 Oct 2026 · Meta's own numbers" />
        <Bars t={b} max={25} w={870} items={[{label: 'Conversions', value: 18.9, color: C.blue}, {label: 'Click-through rate', value: 12, color: C.gold}]} />
        {c >= 0 ? (
          <Row gap={16} align="flex-start">
            <Chip t={c} kind="gold">
              ⚠ Catch
            </Chip>
            <Note t={c} delay={4} size={27}>
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
    const ch = since(beats, frame, 'three-chat');
    const bill = since(beats, frame, 'three-bill');
    return (
      <Col gap={22} style={{alignItems: 'center'}}>
        <Chat t={ch} brand="Your clinic · Diwali offer" adLine="Click-to-WhatsApp ad · Sponsored" reply="Hi! Diwali package ke baare mein batayein?" pill="Free window: up to 7 days" w={600} />
        {bill >= 0 ? (
          <Row gap={16} align="flex-start">
            <Chip t={bill} kind="gold">
              1 OCT 2026
            </Chip>
            <Note t={bill} delay={4} size={27}>
              Service messages charged after 1,000 free / month (WhatsApp pricing page)
            </Note>
          </Row>
        ) : null}
      </Col>
    );
  },

  bonus: ({beats, frame}) => {
    const ch = since(beats, frame, 'bonus-chart');
    const d = since(beats, frame, 'bonus-date');
    return (
      <Col gap={22}>
        <Chart t={ch} w={870} h={300} title="India festive season · Meta ad costs (Criteo, 2025)" note="CPM +26% · CPC +45% vs. pre-festive" points={[[0, 0.18], [0.15, 0.2], [0.3, 0.26], [0.45, 0.38], [0.6, 0.62], [0.72, 0.9], [0.8, 0.84], [0.9, 0.55], [1, 0.3]]} />
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

  cta: ({beats, frame}) => {
    const c = since(beats, frame, 'cta-comment');
    const s = since(beats, frame, 'cta-save');
    return (
      <Col gap={28}>
        <CommentUI t={c} name="Aman Rai" handle="@adsworm · Founder, ADSWORM" keyword="DIWALI" />
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
            <div style={{marginTop: 14}}>
              <PdfCard t={s} title="Diwali Meta Ads Checklist" sub="Free PDF + all official links → in your DM" />
            </div>
          </Col>
        ) : null}
      </Col>
    );
  },
};
