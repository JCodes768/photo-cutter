import argparse
from pathlib import Path

from PIL import Image


def find_vertical_gap_band(image: Image.Image) -> tuple[int, int]:
    """Return (start_x, end_x) for the black film gap between frames."""
    gray = image.convert("L")
    width, height = gray.size

    # Downsample vertically for speed.
    sample_step = max(height // 400, 1)

    mean_by_x = []
    for x in range(width):
        column_sum = 0
        count = 0
        for y in range(0, height, sample_step):
            column_sum += gray.getpixel((x, y))
            count += 1
        mean_by_x.append(column_sum / max(count, 1))

    # Only look near the middle of the scan where the gap normally is.
    start = int(width * 0.25)
    end = int(width * 0.75)
    mid_region = mean_by_x[start:end]
    if not mid_region:
        mid = width // 2
        return max(mid - 2, 0), min(mid + 2, width)

    # Find a dark band (contiguous region of low brightness) in the mid region.
    region_min = min(mid_region)
    threshold = region_min + 5  # a bit above the darkest column

    bands: list[tuple[int, int]] = []
    band_start: int | None = None
    for i, value in enumerate(mid_region):
        x = start + i
        if value <= threshold:
            if band_start is None:
                band_start = x
        else:
            if band_start is not None:
                bands.append((band_start, x - 1))
                band_start = None
    if band_start is not None:
        bands.append((band_start, start + len(mid_region) - 1))

    if not bands:
        mid = width // 2
        return max(mid - 2, 0), min(mid + 2, width)

    # Choose the widest dark band as the film gap.
    gap_start, gap_end = max(bands, key=lambda b: b[1] - b[0])

    # Add a tiny safety margin so we fully remove the gap.
    gap_start = max(gap_start - 2, 0)
    gap_end = min(gap_end + 2, width)
    return gap_start, gap_end


def split_image(
    input_path: Path,
    output_dir: Path,
    crop_border: int = 0,
    overwrite: bool = False,
    auto_gap: bool = False,
) -> None:
    image = Image.open(input_path)
    width, height = image.size

    if auto_gap:
        gap_start, gap_end = find_vertical_gap_band(image)
        left_box = (0, 0, gap_start, height)
        right_box = (gap_end, 0, width, height)
    else:
        # Assume two portrait images side by side in a landscape scan.
        mid_x = width // 2
        left_box = (0, 0, mid_x, height)
        right_box = (mid_x, 0, width, height)

    left = image.crop(left_box)
    right = image.crop(right_box)

    if crop_border > 0:
        def safe_crop(img: Image.Image) -> Image.Image:
            w, h = img.size
            left_c = min(max(crop_border, 0), w // 4)
            top_c = min(max(crop_border, 0), h // 4)
            right_c = min(max(crop_border, 0), w // 4)
            bottom_c = min(max(crop_border, 0), h // 4)
            return img.crop(
                (left_c, top_c, w - right_c, h - bottom_c)
            )

        left = safe_crop(left)
        right = safe_crop(right)

    base_name = input_path.stem
    ext = input_path.suffix or ".jpg"

    left_out = output_dir / f"{base_name}_a{ext}"
    right_out = output_dir / f"{base_name}_b{ext}"

    if not overwrite:
        if left_out.exists() or right_out.exists():
            print(f"Skipping {input_path.name} (output exists). Use --overwrite to replace.")
            return

    left.save(left_out)
    right.save(right_out)
    print(f"Saved {left_out.name} and {right_out.name}")


def process_folder(
    input_dir: Path,
    output_dir: Path,
    crop_border: int,
    overwrite: bool,
    auto_gap: bool,
) -> None:
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    image_extensions = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}
    files = [
        p for p in input_dir.iterdir()
        if p.is_file() and p.suffix.lower() in image_extensions
    ]

    if not files:
        print(f"No image files found in {input_dir}")
        return

    for f in sorted(files):
        try:
            split_image(
                f,
                output_dir,
                crop_border=crop_border,
                overwrite=overwrite,
                auto_gap=auto_gap,
            )
        except Exception as e:
            print(f"Error processing {f.name}: {e}")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Split half-frame scans (two images per JPEG) into separate files."
    )
    parser.add_argument(
        "input",
        type=str,
        help="Folder containing scanned JPEGs (two frames per image).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Output folder for split images (default: <input>\\split).",
    )
    parser.add_argument(
        "--crop-border",
        type=int,
        default=0,
        help="Optional number of pixels to crop from each edge after splitting.",
    )
    parser.add_argument(
        "--auto-gap",
        action="store_true",
        help="Automatically detect the dark film gap between frames instead of splitting exactly in half.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing split files if they already exist.",
    )
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    input_dir = Path(args.input).expanduser().resolve()
    output_dir = Path(args.output).expanduser().resolve() if args.output else input_dir / "split"

    process_folder(
        input_dir=input_dir,
        output_dir=output_dir,
        crop_border=args.crop_border,
        overwrite=args.overwrite,
        auto_gap=args.auto_gap,
    )


if __name__ == "__main__":
    main()

