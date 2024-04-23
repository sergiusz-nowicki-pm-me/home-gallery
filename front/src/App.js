import React, { useEffect, useState } from "react";
import { list_all_galleries } from "./BackendInterface";
import './App.css';
import { GalleryList } from "./GalleryList.js";
import { GalleryPanel } from "./GalleryPanel.js";

function App() {
  const [galleries, setGalleries] = useState({});
  const [selected, setSelected] = useState("");
  const [showThumb, setShowThumb] = useState(false)

  useEffect(() => {
    list_all_galleries()
      .then((m) => {
        setGalleries(m);
        //console.log("galleries loaded: " + JSON.stringify(m));
      })
      .catch((e) => { alert("Error while getting galleries: " + JSON.stringify(e)) })
  }, []);

  return (
    <div>
      <div className="Main-toolbar">
        <label htmlFor="show-thumb">Show thumbs</label>
        <input id="show-thumb" type="checkbox" checked={showThumb} onClick={() => setShowThumb(! showThumb)} />
      </div>
      <div className="Main-panel">
        {selected === ""
          ? <GalleryList galleries={galleries} setSelected={setSelected} showThumb={showThumb} />
          : <GalleryPanel gallery={galleries[selected]} gallery_uuid={selected} clearSelected={() => setSelected("")} showThumb={showThumb} />
        }
      </div>
    </div>
  );
}


export default App;
