def get_lines_from_plaintext(plaintext):
    dirty_lines = plaintext.split("\n")
    return remove_page_markings(dirty_lines)


def remove_blank_lines_from_start_and_end(lines):
    lines_forward = remove_blank_lines_from_start(lines)
    return remove_blank_lines_from_end(lines_forward)


def remove_blank_lines_from_end(lines_forward):
    lines_backward = remove_blank_lines_from_start(reversed(lines_forward))
    return list(reversed(lines_backward))


def remove_blank_lines_from_start(dirty_lines):
    clean_lines = []
    start_recording = False
    for line in dirty_lines:
        if line.strip() != "":
            start_recording = True
        if start_recording:
            clean_lines.append(line)
    return clean_lines


def remove_page_markings(dirty_lines):
    clean_lines = []
    just_removed_page_break = False

    for index, line in enumerate(dirty_lines):

        # After removing each PAGE BREAK, we need to also remove the actual Page Number from the document.
        if just_removed_page_break:

            if line.strip() == "":
                continue

            elif line.strip() != "":
                just_removed_page_break = False

                # If we're at the DOCUMENT END, we don't have a page number to remove.
                if "---- DOCUMENT END ----" in line.strip():
                    clean_lines.append(line)

                continue

        # We need to remove each PAGE BREAK
        if "---- PAGE BREAK ----" in line.strip():
            just_removed_page_break = True
            continue

        clean_lines.append(line)

    return clean_lines

