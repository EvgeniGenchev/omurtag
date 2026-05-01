/* global React, Icon, CopyButton */
const { useState: useStateD } = React;

function QRImage({ addr, size = 200 }) {
  const src = `https://api.qrserver.com/v1/create-qr-code/?size=${size}x${size}&data=${encodeURIComponent(addr)}&margin=8&color=111111&bgcolor=ffffff`;
  return <img src={src} width={size} height={size} alt="QR code" style={{ display: "block", borderRadius: 4 }} />;
}

function DonationModal({ kind, onClose }) {
  const data = kind === "btc"
    ? { sym: "₿", title: "Bitcoin", color: "btc", addr: "bc1q5pdtpvtl7uym0rx6h8av88ruf3zz0kqypwem6r" }
    : { sym: "Ξ", title: "Ethereum", color: "eth", addr: "0x95a14E68E08eEef8AF40cF21fA739dE7B6C73b9b" };
  const [copied, setCopied] = useStateD(false);
  const onCopy = () => {
    navigator.clipboard?.writeText(data.addr).catch(() => {});
    setCopied(true);
    setTimeout(() => setCopied(false), 1400);
  };
  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-head">
          <h3 className="modal-title">
            <span className={`sym ${data.color}`}>{data.sym}</span>
            {data.title}
          </h3>
          <button className="iconbtn" onClick={onClose} aria-label="Close">
            <Icon name="close" size={14} />
          </button>
        </div>
        <div className="qr">
          <QRImage addr={data.addr} size={200} />
        </div>
        <div className="addr">
          <span style={{ flex: 1 }}>{data.addr}</span>
          <button className={copied ? "copied" : ""} onClick={onCopy}>
            {copied ? "✓" : "copy"}
          </button>
        </div>
        <p className="note">Scan or copy the address. Thank you for keeping this tool free and ad-free.</p>
      </div>
    </div>
  );
}

Object.assign(window, { DonationModal, QRImage });
