import React from "react";

export function GallerySummary({ uuid, gallery, setSelected, showThumb }) {
  return <span className="Gallery-summary">
    <button onClick={() => setSelected()}>
      {
        showThumb
          ? <img className="Image-preview-small" src={"http://localhost:8081/image/get-first-thumb/" + uuid} alt={uuid} />
          : ""
      }
      <div>{gallery.path.replace(/^.*[\\/]/, '')}</div>
      <div>{gallery.file_count} images</div>
    </button>
  </span>;
}
