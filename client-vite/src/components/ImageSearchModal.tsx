import { FC, Dispatch, SetStateAction, useState, useEffect } from 'react';
import { Modal, Button, Upload, Image } from 'antd';
import { SearchOutlined, InboxOutlined } from '@ant-design/icons'

type ImageSearchModalProps = {
    open: boolean,
    setPaths: Dispatch<SetStateAction<string[]>>;
    onCancel: () => void;
}

const ImageSearchModal: FC<ImageSearchModalProps> = ({ open, setPaths, onCancel }) => {
    const [uploadImage, setUploadImage] = useState<Blob>();
    const [urlUploadImage, setUrlUploadImage] = useState<string | null>(null);

    const handleSearchImage = () => {
        try {
            const formData = new FormData();
            if (uploadImage) {
                formData.append('image', uploadImage);
                fetch(
                    `${process.env.API_URL}/image_search/`,
                    {
                        method: 'POST',
                        body: formData,
                    }
                ).then(
                    res => res.json()
                ).then(
                    data => setPaths(data["result"])
                )
            } else {
                console.log('No upload image');
            }
        } catch (error) {
            console.log(error);
        }
    }

    useEffect(() => {
        if (uploadImage) {
            const blobUrl = URL.createObjectURL(uploadImage);
            setUrlUploadImage(blobUrl);
        }
    }, [uploadImage])

    useEffect(() => {
        const pasteEvent = (e: ClipboardEvent) => {
            const image = e.clipboardData?.files[0];
            setUploadImage(image);
        }
        document.addEventListener('paste', pasteEvent);

        return () => {
            document.removeEventListener('paste', pasteEvent);
        }
    }, []);

    return (
        <Modal
            open={open}
            title='Image Search'
            onCancel={onCancel}
            footer={<Button icon={<SearchOutlined />} onClick={handleSearchImage}>Search</Button>}
        >
            <Upload.Dragger
                accept='image/png, image/jpeg'
                maxCount={1}
                onChange={(info) => setUploadImage(info.fileList[0]?.originFileObj)}
                beforeUpload={() => false}
            >
                <p className="ant-upload-drag-icon">
                    <InboxOutlined />
                </p>
                <p className="ant-upload-text">Paste an image or Click / drag file to this area to upload</p>
            </Upload.Dragger>
            {urlUploadImage && <Image src={urlUploadImage} />}
        </Modal>
    )
}

export default ImageSearchModal;