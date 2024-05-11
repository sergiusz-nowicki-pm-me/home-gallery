import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { ImageSetPanel } from "./pages/gallery/ImageSetPanel";
import { ImagePanel } from "./pages/gallery/ImagePanel";
import { MainPage } from "./MainPage";

import "./index.css";

const router = createBrowserRouter([
    {
        path: "/",
        element: <MainPage />,
        errorElement: <div>error</div>,
        children: [
            {
                path: "gallery/:id",
                element: <ImageSetPanel />,
            },
            {
                path: "gallery/:id/:file_no/:max_file_no",
                element: <ImagePanel />,
            },
        ],
    },
]);

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
    <React.StrictMode>
        <RouterProvider router={router} />
    </React.StrictMode>
);
