type IProps = {
    className?: string;
    label: string;
    handleOnChange(label: string): void;
    isChecked?: boolean;
}

const Checkbox = ({ className, label, handleOnChange, isChecked }: IProps) => {

    const toggleCheckboxChange = () => {
        handleOnChange(label)
    }

    return (
      <div className={className}>
          <label>
              <input
                  type="checkbox"
                  value={label}
                  checked={isChecked}
                  onChange={toggleCheckboxChange}
                  data-testid="checkbox"
                />

              <span className="checkmark">{label}</span>
            </label>
        </div>
    )
}

export default Checkbox
