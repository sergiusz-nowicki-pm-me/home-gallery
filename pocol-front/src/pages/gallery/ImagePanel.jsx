import { useNavigate, useParams } from "react-router-dom";
import { BASE_URL } from "../../consts";
import Carousel, { Modal, ModalGateway } from "react-images";

export function ImagePanel() {
    let { id, file_no, max_file_no } = useParams();
    const navigate = useNavigate();

    const photos = [];
    for (let i = 0; i <= max_file_no; i++) {
        photos.push({ src: BASE_URL + "/image/" + id + "/" + i });
    }

    const closeLightbox = () => {
        navigate("/gallery/" + id);
    };

    return (
        <ModalGateway>
            <Modal onClose={closeLightbox}>
                <Carousel currentIndex={file_no} views={photos} />
            </Modal>
        </ModalGateway>
    );
    // <img src={BASE_URL + "/image/" + id + "/" + file_no} />;
}
