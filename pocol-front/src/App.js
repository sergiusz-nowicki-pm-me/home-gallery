import React, { useEffect, useState } from "react";
import { list_all_galleries } from "./BackendInterface";
import "./App.css";
import { GalleryList } from "./GalleryList.js";
import { GalleryPanel } from "./GalleryPanel.js";
import ResizePanel from "react-resize-panel";

function App() {
    const [galleries, setGalleries] = useState({});
    const [selected, setSelected] = useState("");
    const [showThumb, setShowThumb] = useState(false);

    const [pageGalleryCount, setPageGalleryCount] = useState(25);

    useEffect(() => {
        list_all_galleries()
            .then((m) => {
                setGalleries(m);
            })
            .catch((e) => {
                alert("Error while getting galleries: " + JSON.stringify(e));
            });
    }, []);

    return (
        <div className="Main-layout">
            <div className="Main-toolbar">
                <div>
                    <label htmlFor="show-thumb">Show thumbs</label>
                    <input
                        id="show-thumb"
                        type="checkbox"
                        checked={showThumb}
                        onClick={() => setShowThumb(!showThumb)}
                    />
                </div>
                <div>
                    <PageGalleryCount setCount={setPageGalleryCount} />
                </div>
            </div>
            <div className="Main-panel">
                {selected === "" ? (
                    <GalleryList
                        galleries={galleries}
                        setSelected={setSelected}
                        showThumb={showThumb}
                    />
                ) : (
                    <GalleryPanel
                        gallery={galleries[selected]}
                        gallery_uuid={selected}
                        clearSelected={() => setSelected("")}
                        showThumb={showThumb}
                    />
                )}
            </div>
        </div>
    );
}

export function PageGalleryCount({ setCount }) {
    return (
        <select>
            <option value="25" onSelect={() => setCount(25)}>
                25
            </option>
            <option value="50" onSelect={() => setCount(50)}>
                50
            </option>
            <option value="75" onSelect={() => setCount(75)}>
                75
            </option>
            <option value="100" onSelect={() => setCount(100)}>
                100
            </option>
        </select>
    );
}

export default App;
