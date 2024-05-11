import axios from "axios";
import { useCallback, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Gallery from "react-photo-gallery";
import { BASE_URL } from "../../consts";

export function ImageSetPanel() {
    const navigate = useNavigate();
    let { id } = useParams();
    const [photos, setPhotos] = useState([]);
    let cnt = 0;

    useEffect(() => {
        const imageSetLoader = async (id) => {
            let responce = await axios.get(
                "http://localhost:8081/query/get-image-set/" + id
            );
            console.log(responce);
            const imgs = Object.keys(responce.data.data.images).map((f) => {
                return {
                    src: `${BASE_URL}/image/${id}/${f}`,
                };
            });
            cnt = imgs.length - 1;
            setPhotos(imgs);
        };
        imageSetLoader(id);
    }, [id]);

    const openLightbox = useCallback((event, { photo, index }) => {
        navigate(`/gallery/${id}/${index}/${cnt}`);
    }, []);

    return (
        <div>
            Test: {id}
            <Gallery
                photos={photos}
                targetRowHeight={256}
                onClick={openLightbox}
            />
        </div>
    );
}
