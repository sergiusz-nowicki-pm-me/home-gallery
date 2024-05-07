import React from "react";
import { GallerySummary } from "./GallerySummary.js";

export function GalleryList({ galleries, setSelected, showThumb }) {
  return <React.Fragment>
    {Object.keys(galleries)
    .sort((a, b) => {
      const name1 = galleries[a].path.replace(/^.*[\\/]/, '');
      const name2 = galleries[b].path.replace(/^.*[\\/]/, '');
      return name1 < name2 ? -1 : 1;
    })
    .map((v) => {
      return <GallerySummary key={v} uuid={v} gallery={galleries[v]} setSelected={() => setSelected(v)} showThumb={showThumb} />;
    })}
  </React.Fragment>;
}
