import express from "express";
import cors from "cors";
import path from "path";
import { fileURLToPath } from "url";
import fetch from "node-fetch";
import Razorpay from "razorpay";
import JSZip from "jszip";
import crypto from "crypto";
import dotenv from "dotenv";

dotenv.config();

const app = express();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PYTHON_API_BASE = process.env.PYTHON_API_BASE;
const RAZORPAY_KEY_ID = process.env.RAZORPAY_KEY_ID;
const RAZORPAY_KEY_SECRET = process.env.RAZORPAY_KEY_SECRET;

const corsOptions = {
  origin: [
    "https://render-recorn.vercel.app",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
  ],
  methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
  allowedHeaders: ["Content-Type", "Authorization", "X-Requested-With"],
  credentials: true,
  optionsSuccessStatus: 200
};

app.use(cors(corsOptions));
app.use(express.json({ limit: "50mb" }));

const publicPath = path.join(process.cwd(), "public");
app.use(express.static(publicPath));

app.get("/", (req, res) => {
  res.sendFile(path.join(publicPath, "index.html"));
});

// Proxy route to Python Backend
app.post("/api/generate", async (req, res) => {
  try {
    const { target_url } = req.body || {};
    if (!target_url) {
      return res.status(400).json({ error: "target_url is required" });
    }

    const response = await fetch(`${PYTHON_API_BASE}/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ target_url }),
    });

    if (!response.ok) {
      const text = await response.text();
      return res
        .status(response.status)
        .json({ error: "Python backend error", details: text });
    }

    const data = await response.json();
    return res.json({
      structure_md: data.structure_md,
      design_md: data.design_md,
      usecase_md: data.usecase_md,
    });
  } catch (err) {
    console.error("[Node API] /api/generate error:", err);
    res.status(500).json({ error: "Internal server error" });
  }
});

// Razorpay: Create Order
app.post("/api/create-order", async (req, res) => {
  try {
    if (!RAZORPAY_KEY_ID || !RAZORPAY_KEY_SECRET) {
      return res.status(500).json({
        error: "Razorpay keys are missing from server environment.",
      });
    }

    const { amount, currency } = req.body || {};
    const finalAmount = amount || 100000; // ₹1,000 in paise
    const finalCurrency = currency || "INR";

    const instance = new Razorpay({
      key_id: RAZORPAY_KEY_ID,
      key_secret: RAZORPAY_KEY_SECRET,
    });

    const options = {
      amount: finalAmount,
      currency: finalCurrency,
      receipt: `rcpt_${Date.now()}`,
    };

    const order = await instance.orders.create(options);

    return res.json({
      id: order.id,
      amount: order.amount,
      currency: order.currency,
      keyId: RAZORPAY_KEY_ID,
    });
  } catch (err) {
    console.error("[Node API] /api/create-order error:", err);
    res.status(500).json({ error: err.message || "Failed to create Razorpay order" });
  }
});

// Razorpay: Verify Payment Signature
app.post("/api/verify-payment", async (req, res) => {
  try {
    if (!RAZORPAY_KEY_SECRET) {
      return res.status(500).json({
        verified: false,
        error: "Razorpay secret key is not configured on the server.",
      });
    }

    const { razorpay_order_id, razorpay_payment_id, razorpay_signature } = req.body || {};

    if (!razorpay_order_id || !razorpay_payment_id || !razorpay_signature) {
      return res.status(400).json({
        verified: false,
        error: "Missing required payment verification parameters.",
      });
    }

    const generatedSignature = crypto
      .createHmac("sha256", RAZORPAY_KEY_SECRET)
      .update(`${razorpay_order_id}|${razorpay_payment_id}`)
      .digest("hex");

    if (generatedSignature !== razorpay_signature) {
      return res.status(400).json({
        verified: false,
        error: "Cryptographic signature mismatch. Verification failed.",
      });
    }

    return res.json({
      verified: true,
      message: "Payment signature verified successfully.",
      paymentId: razorpay_payment_id,
    });
  } catch (err) {
    console.error("[Node API] /api/verify-payment error:", err);
    return res.status(500).json({ verified: false, error: "Payment verification error." });
  }
});

// Generate ZIP package using JSZip
app.post("/api/generate-zip", async (req, res) => {
  try {
    const { structure_md, design_md, usecase_md } = req.body || {};

    if (!structure_md || !design_md || !usecase_md) {
      return res.status(400).json({
        error: "ZIP_INPUT_ERROR",
        message: "All three markdown contents are required to generate the ZIP file.",
      });
    }

    const zip = new JSZip();
    zip.file("structure.md", structure_md);
    zip.file("design.md", design_md);
    zip.file("usecase.md", usecase_md);

    const zipBuffer = await zip.generateAsync({
      type: "nodebuffer",
      compression: "DEFLATE",
      compressionOptions: { level: 9 },
    });

    res.setHeader("Content-Type", "application/zip");
    res.setHeader(
      "Content-Disposition",
      'attachment; filename="render_recorn_specs.zip"'
    );
    res.setHeader("Content-Length", zipBuffer.length);

    return res.send(zipBuffer);
  } catch (err) {
    console.error("[Node API] /api/generate-zip unexpected error:", err);
    return res.status(500).json({
      error: "ZIP_INTERNAL_ERROR",
      message: err.message || "Failed to generate ZIP file.",
    });
  }
});

if (process.env.VERCEL !== "1") {
  const port = process.env.PORT || 3000;
  app.listen(port, () => {
    console.log(`Express server running on http://localhost:${port}`);
  });
}

export default app;