import { useParams } from "react-router-dom";
import { BASE_URL } from "../../consts";

export function ImagePanel() {
    let { id, file_no } = useParams();

    return <img src={BASE_URL + "/image/" + id + "/" + file_no} />;
}
