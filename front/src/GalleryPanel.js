import React, { useCallback, useEffect, useState } from "react";
import Carousel, { Modal, ModalGateway } from "react-images";
import { gallery } from "./BackendInterface.js";
import { Loader } from "./Loader.js";
import Gallery from "react-photo-gallery";

export function GalleryPanel({ gallery_uuid, clearSelected }) {
  const [loading, setLoading] = useState(true);
  const [previews, setPreviews] = useState([]);
  const [photos, setPhotos] = useState([]);

  useEffect(() => {
    setLoading(true);
    gallery(gallery_uuid)
      .then((v) => {
        const ids = Object.keys(v.files)
        .sort((a, b) => {
          const name1 = v.files[a].path.replace(/^.*[\\/]/, '')
          const name2 = v.files[b].path.replace(/^.*[\\/]/, '')
          return name1 < name2 ? -1 : 1;
        });

        const ph = ids.map((f) => {
          const obj = {...v.files[f]};
          obj["src"] = `http://localhost:8081/image/get/${gallery_uuid}/${f}`;
          return obj;
        });
        setPhotos(ph);

        const pre = ids.map((f) => {
          const obj = {...v.files[f]};
          obj["src"] = `http://localhost:8081/image/get-thumb/${gallery_uuid}/${f}`;
          return obj;
        });
        setPreviews(pre)

        setLoading(false);
      })
      .catch((e) => alert(e))
  }, [gallery_uuid]);

  const [currentImage, setCurrentImage] = useState(0);
  const [viewerIsOpen, setViewerIsOpen] = useState(false);

  const openLightbox = useCallback((event, { photo, index }) => {
    setCurrentImage(index);
    setViewerIsOpen(true);
  }, []);

  const closeLightbox = () => {
    setCurrentImage(0);
    setViewerIsOpen(false);
  };

  return <div>
    <div className="Gallery-panel-toolbar">
      <button onClick={() => clearSelected()}>Zamknij</button>
    </div>
    {/* <div className="Gallery-panel-main"> */}
    {loading
      ? <Loader />
      : <React.Fragment>
        <div className="Gallery-panel-main">
          <Gallery photos={previews} targetRowHeight={256} onClick={openLightbox} />
          <ModalGateway>
            {viewerIsOpen ? (
              <Modal onClose={closeLightbox}>
                <Carousel
                  currentIndex={currentImage}
                  views={photos}
                />
              </Modal>
            ) : null}
          </ModalGateway>
        </div>
      </React.Fragment>
    }
    {/* </div> */}
  </div>;
}


