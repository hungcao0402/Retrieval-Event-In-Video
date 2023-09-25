import { Dispatch, SetStateAction, useState, FC, useEffect } from 'react';
import { Row, Col, Input, InputNumber, Button } from 'antd';
import { SearchOutlined, PlusOutlined, DeleteOutlined, CameraOutlined } from '@ant-design/icons';
import { ImageSearchModal } from '.'



type TextQuery = {
    text: string,
    top_k: number,
}

const blankTextQuery: TextQuery = { text: '', top_k: 100 }

type QueryFormProps = {
    setPaths: Dispatch<SetStateAction<string[]>>;
    positiveFrames: string[];
    negativeFrames: string[];
    resetFeedback: () => void;
};

const QueryForm: FC<QueryFormProps> = ({ setPaths, positiveFrames, negativeFrames, resetFeedback }) => {
    const [captions, setCaptions] = useState<TextQuery[]>([blankTextQuery]);
    const [ocr, setOcr] = useState<TextQuery>(blankTextQuery);
    const [asr, setAsr] = useState<TextQuery>(blankTextQuery);
    const [finalTopK, setFinalTopK] = useState<number>(500);

    const [loading, setLoading] = useState<boolean>(false);

    const [imageSearchModalOpen, setImageSearchModelOpen] = useState(false);

    const handleAddCaption = () => {
        const updatedCaptions = [...captions, blankTextQuery];
        setCaptions(updatedCaptions);
    }

    const handleCaptionChange = (text: string, index: number) => {
        const updatedCaption = {
            ...captions[index],
            text: text
        }
        const updatedCaptions = [...captions];
        updatedCaptions[index] = updatedCaption;
        setCaptions(updatedCaptions);
    }

    const handleTopKChange = (value: number | null, index: number) => {
        if (value !== null) {
            const updatedCaption: TextQuery = {
                ...captions[index],
                top_k: value
            }
            const updatedCaptions = [...captions];
            updatedCaptions[index] = updatedCaption;
            setCaptions(updatedCaptions);
        }
    }

    const handleDeleteCaption = (index: number) => {
        const updatedCaptions = [...captions];
        updatedCaptions.splice(index, 1);
        setCaptions(updatedCaptions)
    }

    const handleOcrChange = (text: string) => {
        const updatedOcr: TextQuery = {
            ...ocr,
            text: text
        }
        setOcr(updatedOcr);
    }

    const handleOcrTopKChange = (value: number | null) => {
        if (value !== null) {
            const updatedOcr: TextQuery = {
                ...ocr,
                top_k: value
            }
            setOcr(updatedOcr);
        }
    }

    const handleAsrChange = (text: string) => {
        const updatedAsr: TextQuery = {
            ...asr,
            text: text
        }
        setAsr(updatedAsr);
    }

    const handleAsrTopKChange = (value: number | null) => {
        if (value !== null) {
            const updatedAsr: TextQuery = {
                ...asr,
                top_k: value
            }
            setAsr(updatedAsr);
        }
    }

    const handleFinalTopKChange = (v: number | null) => {
        if (v !== null) {
            setFinalTopK(v);
        }
    }

    const handleSearch = async () => {
        try {
            const textQueryForm = {
                clip_queries: captions,
                ocr_query: ocr,
                asr_query: asr,
                final_top_k: finalTopK,
                positive_frames: positiveFrames,
                negative_frames: negativeFrames,
            }

            console.log('query form', textQueryForm)
            setLoading(true);
            fetch(
                `${process.env.API_URL}/search`,
                {
                    method: "POST",
                    headers: {
                        'content-type': 'application/json',
                    },
                    body: JSON.stringify(textQueryForm)
                }
            ).then(
                res => res.json()
            ).then(
                data => setPaths(data['result'])
            )
        } catch (error) {
            console.log(error);
        } finally {
            setLoading(false);
        }
    }

    const handleResetTextQueryForm = () => {
        setCaptions([blankTextQuery]);
        setOcr(blankTextQuery);
        setAsr(blankTextQuery);
        setFinalTopK(500);
        resetFeedback();
    }

    // Enter to search
    useEffect(() => {
        const onEnter = (e: KeyboardEvent) => {
            if (e.key == "Enter") {
                handleSearch();
            }
        }
        document.addEventListener("keydown", onEnter);
        return () => {
            document.removeEventListener("keydown", onEnter);
        }
    },)

    return (
        <Row style={{ padding: '10px 30px' }}>
            <Col span={18} className='flex-col'>
                <div className='flex-row' >
                    <div className='flex-col'>
                        {captions && captions.map((caption, index) => (
                            <div className='flex-row' key={index}>
                                <Input
                                    placeholder='Text query'
                                    value={caption.text}
                                    onChange={(e) => handleCaptionChange(e.target.value, index)}
                                />
                                <InputNumber
                                    min={1}
                                    max={10000}
                                    defaultValue={100}
                                    step={50}
                                    onChange={(v) => handleTopKChange(v, index)}
                                    value={caption.top_k}
                                />
                                <Button
                                    icon={<DeleteOutlined />}
                                    onClick={() => handleDeleteCaption(index)}
                                    disabled={captions.length <= 1}
                                />
                            </div>
                        ))}
                    </div>
                    <Button icon={<PlusOutlined />} onClick={handleAddCaption} />
                </div>

                <div className='flex-col'>
                    <div className='flex-row'>
                        <Input
                            placeholder='OCR query'
                            onChange={(e) => handleOcrChange(e.target.value)}
                            value={ocr.text}
                        />
                        <InputNumber
                            min={1}
                            max={10000}
                            defaultValue={100}
                            step={50}
                            onChange={(v) => handleOcrTopKChange(v)}
                        />
                    </div>
                    <div className='flex-row'>
                        <Input
                            placeholder='ASR query'
                            onChange={(e) => handleAsrChange(e.target.value)}
                            value={asr.text}
                        />
                        <InputNumber
                            min={1}
                            max={10000}
                            defaultValue={100}
                            step={50}
                            onChange={(v) => handleAsrTopKChange(v)}
                        />
                    </div>
                </div>
            </Col>

            <Col span={6} style={{ padding: '10px 30px' }}>
                <div className='flex-col' >
                    <Button icon={<CameraOutlined />} onClick={() => setImageSearchModelOpen(true)} />
                    <ImageSearchModal open={imageSearchModalOpen} setPaths={setPaths} onCancel={() => setImageSearchModelOpen(false)} />
                    <div className='flex-row' >
                        <span>Top K</span>
                        <InputNumber min={1} max={1000} defaultValue={finalTopK} step={10} onChange={handleFinalTopKChange} />
                    </div>
                    <div className='flex-row' >
                        <Button type="primary" icon={<SearchOutlined />} loading={loading} onClick={handleSearch}>Search</Button>
                        <Button icon={<DeleteOutlined />} onClick={handleResetTextQueryForm}>Reset</Button>
                    </div>
                </div>
            </Col>
        </Row>
    )
}

export default QueryForm