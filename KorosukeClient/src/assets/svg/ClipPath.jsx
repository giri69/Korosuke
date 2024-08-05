const ClipPath = () => {
  return (
    <svg className="block" width={0} height={0}>
      <clipPath id="benefits" clipPathUnits="objectBoundingBox">
        <rect x="0" y="0" width="1" height="1" rx="0.1" ry="0.1" />
      </clipPath>
    </svg>
  );
};

export default ClipPath;
