export default function LoadingSkeleton() {
  return (
    <div className="skeleton-panel" role="status" aria-label="Loading">
      <div className="skeleton-line skeleton-line--lg" />
      <div className="skeleton-line skeleton-line--md" />
      <div className="skeleton-block" />
      <div className="skeleton-row">
        <div className="skeleton-button" />
        <div className="skeleton-line skeleton-line--sm" />
      </div>
    </div>
  );
}
